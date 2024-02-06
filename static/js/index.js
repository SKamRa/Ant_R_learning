let i = 1;

function myLoop(nb_turn) {
  setTimeout(function() {
    let filename = "static/frames/frame" + i + ".jpg";
    document.getElementById("frame").src=filename;
    i++;
    if (i < 10) {
      myLoop();
    }
  }, 500)
}