// Optional: Scroll animation for articles
const articles = document.querySelectorAll('.article-list article');
window.addEventListener('scroll', () => {
  const triggerBottom = window.innerHeight / 5 * 4;
  articles.forEach(article => {
    const articleTop = article.getBoundingClientRect().top;
    if(articleTop < triggerBottom) {
      article.style.transform = 'translateY(0)';
      article.style.opacity = '1';
    } else {
      article.style.transform = 'translateY(50px)';
      article.style.opacity = '0';
    }
  });
});

// Initialize articles with hidden state
articles.forEach(article => {
  article.style.transform = 'translateY(50px)';
  article.style.opacity = '0';
  article.style.transition = 'all 0.6s ease-out';
});
