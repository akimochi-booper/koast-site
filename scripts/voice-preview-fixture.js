// Local preview only: labelled synthetic recognition and oscillator signal; no microphone access.
(function(){
  var RealAudio=window.AudioContext||window.webkitAudioContext;
  window.SpeechRecognition=class {
    start(){this.ended=false;setTimeout(()=>{if(this.ended)return;this.onstart?.();this.timer=setTimeout(()=>{if(!this.ended)this.onresult?.({results:[[{transcript:'Move pickup to six'}]]});},800);},0);}
    stop(){clearTimeout(this.timer);this.ended=true;this.onend?.();}
    abort(){clearTimeout(this.timer);this.ended=true;}
  };
  if(RealAudio){Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:async function(){var context=new RealAudio(),oscillator=context.createOscillator(),gain=context.createGain(),destination=context.createMediaStreamDestination();oscillator.frequency.value=180;gain.gain.value=.3;oscillator.connect(gain);gain.connect(destination);oscillator.start();await context.resume();var tracks=destination.stream.getTracks();tracks.forEach(function(track){var stop=track.stop.bind(track);track.stop=function(){stop();oscillator.stop();context.close();};});return destination.stream;}}});}
})();
