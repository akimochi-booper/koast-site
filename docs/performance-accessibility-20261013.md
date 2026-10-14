# Airport, performance and accessibility release — 2026-10-13

Airport content: see airport-pages-20261013.md. Global changes preserve the existing design while improving contrast, focus handling and loading.

Performance: self-host unmodified Plus Jakarta Sans Latin variable font with OFL notice, preload and font-display swap; native lazy carousel images with the same overlays; load the Moovs iframe when it approaches the viewport (or receives keyboard focus), with direct booking and no-script links retained. This does not reduce Moovs' own application payload once it loads.

Accessibility: dark text on orange buttons; darker orange prose links; brighter footer text; 44px carousel pagination controls; hidden photo arrows disabled; Escape dismisses desktop navigation; modal background is inert and photo Tab navigation contained; chat reply live regions; phone inputs 16px; prose links underlined; repaired 404 landmark and navigation/footer labels.

Baseline SJC PageSpeed mobile, Oct 13 18:31 PDT: Performance 52, Accessibility 90, Best Practices 92, SEO 100. FCP 25.9s, LCP 31.5s, TBT 200ms, CLS 0. Slow-4G simulated lab run; no field data. Report: https://pagespeed.web.dev/analysis/https-koastride-com-airports-sjc/h9it6ysulx?form_factor=mobile

Validation before release: 203 generated pages checked; 16 Node tests passed (13 tracking, 3 booking loading); 14 unique inline scripts parsed. Direct Chrome desktop/390px/320px checks covered SJC/OAK content, booking render, menu Escape, photo focus loop/restoration, inert chat background, input sizing and absence of horizontal page overflow. Live after-release metrics are recorded in the project audit.

Limitations: automated checks do not certify WCAG conformance; no dedicated screen-reader user test; cross-origin Moovs interface remains externally maintained. Booking-click tracking is intent, not reservations or revenue. Search effect requires later Search Console comparison.
