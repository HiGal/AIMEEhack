var record = document.querySelector("#mic");
var state = 0;

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
   console.log('getUserMedia supported.');
   navigator.mediaDevices.getUserMedia (
      // constraints - only audio needed for this app
      {
         audio: true
      })

      // Success callback
      .then(function(stream) {
          var mediaRecorder = new MediaRecorder(stream);

          record.onclick = function() {
              if(state === 0) {
                  mediaRecorder.start();
                  console.log(mediaRecorder.state);
                  console.log("recorder started");
                  record.style.color = "red";
                  state++;
              }else if(state === 1){
                  mediaRecorder.stop();
                  console.log(mediaRecorder.state);
                  console.log("recorder stopped");
                  record.style.background = "";
                  record.style.color = "";
                  state = 0;
              }
          };


          mediaRecorder.addEventListener("dataavailable", onRecordingReady);

      })

      // Error callback
      .catch(function(err) {
         console.log('The following getUserMedia error occured: ' + err);
      }
   );

   function onRecordingReady(e) {
         var audio = document.getElementById('audio');
         // e.data contains a blob representing the recording
         audio.src = URL.createObjectURL(e.data);
         audio.play();
         var formData = new FormData();
         var fileType = 'audio';
         var fileName = 'output.wav';
         formData.append(fileType, e.data, fileName);
         $.ajax({
            type: 'POST',
            url: 'http://localhost/',
            data: formData,
            processData: false,  // prevent jQuery from converting the data
            contentType: false,  // prevent jQuery from overriding content type
            success: function(response) {
            alert(response);
    }
});
}

} else {
   console.log('getUserMedia not supported on your browser!');
}
