
const menuBtn = document.getElementById("menuBtn");
const mainNav = document.getElementById("mainNav");

if (menuBtn && mainNav) {
  menuBtn.addEventListener("click", () => {
    mainNav.classList.toggle("open");
    menuBtn.textContent = mainNav.classList.contains("open") ? "✕" : "☰";
  });
}

document.querySelectorAll(".news-card, .trend-item").forEach((card) => {
  card.addEventListener("mouseenter", () => card.classList.add("active"));
  card.addEventListener("mouseleave", () => card.classList.remove("active"));
});
