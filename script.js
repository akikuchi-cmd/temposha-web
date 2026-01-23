document.addEventListener('DOMContentLoaded', () => {

    // --- カテゴリ切り替え機能 ---
    const buttons = document.querySelectorAll('.cat-btn');
    const sections = document.querySelectorAll('.work-section');

    if (buttons.length > 0) {
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const targetId = btn.getAttribute('data-target');
                sections.forEach(sec => sec.classList.remove('active'));

                const targetSection = document.getElementById(targetId);
                if (targetSection) {
                    targetSection.classList.add('active');
                }
            });
        });
    }

    // --- ヘッダースクロール検知 ---
    const header = document.querySelector('.top_menu001');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        });
    }
});