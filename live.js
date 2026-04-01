const container = document.querySelector(".container");
const mainVideo = container.querySelector("video");
const progressBar = container.querySelector(".progress-bar");
const playPauseBtn = container.querySelector(".play-pause i");
const volumeBtn = container.querySelector(".volume i");
const volumeSlider = container.querySelector("input");
const fullScreenBtn = container.querySelector(".fullscreen i");
const logo = container.querySelector(".video-logo");

let timer;

/* Hide controls */
const hideControls = () => {
  if (mainVideo.paused) return;

  timer = setTimeout(() => {
    container.classList.remove("show-controls");

    // ✅ keep logo visible
    if (logo) logo.style.opacity = "0.5";

  }, 3000);
};

hideControls();

/* Show controls on mouse move */
container.addEventListener("mousemove", () => {
  container.classList.add("show-controls");
  clearTimeout(timer);

  if (logo) logo.style.opacity = "1";

  hideControls();
});

/* Play / Pause */
playPauseBtn.addEventListener("click", () => {
  if (mainVideo.paused) {
    mainVideo.play();
  } else {
    mainVideo.pause();
  }
});

mainVideo.addEventListener("play", () => {
  playPauseBtn.classList.replace("fa-play", "fa-pause");
});

mainVideo.addEventListener("pause", () => {
  playPauseBtn.classList.replace("fa-pause", "fa-play");
});

/* Volume */
volumeBtn.addEventListener("click", () => {
  if (mainVideo.volume > 0) {
    mainVideo.volume = 0;
    volumeBtn.classList.replace("fa-volume-high", "fa-volume-xmark");
  } else {
    mainVideo.volume = 1;
    volumeBtn.classList.replace("fa-volume-xmark", "fa-volume-high");
  }
});

/* Volume slider */
volumeSlider.addEventListener("input", e => {
  mainVideo.volume = e.target.value;
});

/* Progress */
mainVideo.addEventListener("timeupdate", () => {
  const percent = (mainVideo.currentTime / mainVideo.duration) * 100;
  progressBar.style.width = percent + "%";
});

/* Fullscreen */
fullScreenBtn.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    container.requestFullscreen();
    fullScreenBtn.classList.replace("fa-expand", "fa-compress");
  } else {
    document.exitFullscreen();
    fullScreenBtn.classList.replace("fa-compress", "fa-expand");
  }
});
