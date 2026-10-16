// Koast AI Chat â€” Cloudflare Worker (v2: self-updating facts)
// Proxies chat requests to the Claude API. The API key lives in a Worker
// secret named ANTHROPIC_API_KEY (Settings â†’ Variables and Secrets).
//
// v2: facts are no longer hardcoded. On every request the Worker pulls
// https://koastride.com/llms.txt (cached at the edge for 1 hour) â€” that file
// is regenerated from the site's data on every deploy, so the agent always
// knows the current cities, airports, fleet, and wineries automatically.

const ALLOWED_ORIGINS = [
  "https://koastride.com",
  "https://www.koastride.com",
];

const FACTS_URL = "https://koastride.com/llms.txt";

// Minimal fallback if the facts file can't be fetched
const FALLBACK_FACTS = `Koast is a professional chauffeured black-car service headquartered in San Francisco, serving major US cities nationwide, 24/7. Flat-rate all-inclusive pricing, no surge. Airport transfers with live flight tracking and free wait time (30 min domestic / 60 min international), corporate travel, wine tours, events. Booking: https://customer.moovs.app/koast/request/new. Contact: TEXT (650) 880-6514 or reserve@koastride.com.`;

const RULES = `

RULES:
1. Answer ONLY from the facts above. Never invent prices, dollar amounts, or exact cancellation windows. For prices, always point to the instant-quote widget on the page or the booking link.
2. You cannot make, change, or cancel bookings. Direct riders to the booking widget, the rider portal (https://customer.moovs.app/koast/new/info), or texting (650) 880-6514.
3. If a question is outside these facts (complaints, refunds, specific reservations, anything personal), say a human can help fastest and give the text number.
4. Keep answers to 1-3 short sentences. Be warm and direct.
5. PLAIN TEXT ONLY: never use asterisks, markdown formatting, bullet symbols, or headers. Write in plain sentences.
6. Stay on topic: Koast and ground transportation. Politely decline anything else.`;

const INTRO = `You are the Koast assistant â€” a friendly, concise helper on koastride.com, the website of Koast, a professional chauffeured black-car service. Motto: "Ride easy."

FACTS YOU KNOW (answer ONLY from these):
`;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const corsOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
    const cors = {
      "Access-Control-Allow-Origin": corsOrigin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST")
      return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: { ...cors, "Content-Type": "application/json" } });

    let body;
    try { body = await request.json(); } catch {
      return new Response(JSON.stringify({ error: "Bad JSON" }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } });
    }

    // sanitize: cap history to last 12 turns, each message to 1000 chars
    const messages = (Array.isArray(body.messages) ? body.messages : [])
      .slice(-12)
      .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
      .map(m => ({ role: m.role, content: m.content.slice(0, 1000) }));

    if (!messages.length || messages[messages.length - 1].role !== "user")
      return new Response(JSON.stringify({ error: "No user message" }), { status: 400, headers: { ...cors, "Content-Type": "application/json" } });

    // Live facts: fetch the site's fact sheet, cached at the edge for 1 hour
    let facts = FALLBACK_FACTS;
    try {
      const fr = await fetch(FACTS_URL, { cf: { cacheTtl: 3600, cacheEverything: true } });
      if (fr.ok) {
        const t = await fr.text();
        if (t && t.length > 200) facts = t.slice(0, 24000);
      }
    } catch (e) { /* fall back silently */ }

    const fallback = () => new Response(JSON.stringify({ error: "upstream", reply: "Sorry — I'm having trouble right now. Text us at (650) 880-6514 and a human will help right away." }),
      { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
    if (!env.OPENAI_API_KEY) return fallback();
    const model = env.OPENAI_CHAT_MODEL || "gpt-6-luna";
    try {
      const apiRes = await fetch("https://api.openai.com/v1/responses", {
        method: "POST",
        headers: { Authorization: "Bearer " + env.OPENAI_API_KEY, "Content-Type": "application/json" },
        body: JSON.stringify({
          model,
          store: false,
          reasoning: { effort: "low" },
          max_output_tokens: 1024,
          instructions: INTRO + facts + RULES,
          input: messages,
        }),
        signal: AbortSignal.timeout(30000),
      });
      if (!apiRes.ok) return fallback();
      const data = await apiRes.json();
      if (data.status !== "completed") return fallback();
      const reply = (data.output || []).filter(item => item.type === "message")
        .flatMap(item => item.content || []).filter(part => part.type === "output_text")
        .map(part => part.text).join("\n").trim();
      if (!reply) return fallback();
      return new Response(JSON.stringify({ reply }), { headers: {
        ...cors, "Content-Type": "application/json", "X-Koast-AI-Provider": "openai",
        "X-Koast-AI-Model": data.model || model,
      } });
    } catch {
      return fallback();
    }
  },
};
