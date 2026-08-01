
const menuBtn = document.getElementById("menuBtn");
const mainNav = document.getElementById("mainNav");

let backdrop = document.querySelector(".mobile-menu-backdrop");

if (!backdrop) {
  backdrop = document.createElement("div");
  backdrop.className = "mobile-menu-backdrop";
  document.body.appendChild(backdrop);
}

function closeMenu() {
  if (!mainNav || !menuBtn) return;
  mainNav.classList.remove("open");
  backdrop.classList.remove("show");
  document.body.classList.remove("menu-open");
  menuBtn.textContent = "☰";
  menuBtn.setAttribute("aria-expanded", "false");
}

function openMenu() {
  if (!mainNav || !menuBtn) return;
  mainNav.classList.add("open");
  backdrop.classList.add("show");
  document.body.classList.add("menu-open");
  menuBtn.textContent = "✕";
  menuBtn.setAttribute("aria-expanded", "true");
}

if (menuBtn && mainNav) {
  menuBtn.setAttribute("aria-expanded", "false");

  menuBtn.addEventListener("click", () => {
    mainNav.classList.contains("open") ? closeMenu() : openMenu();
  });

  backdrop.addEventListener("click", closeMenu);

  mainNav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", closeMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 960) closeMenu();
  });

  document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu();
  });
}
