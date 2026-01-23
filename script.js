document.addEventListener('DOMContentLoaded', () => {

    // --- Workページのタブ切り替え ---
    const buttons = document.querySelectorAll('.cat-btn');
    const sections = document.querySelectorAll('.work-section');

    if (buttons.length > 0) {
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
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

    // --- スマホ用ハンバーガーメニュー ---
    const menuBtn = document.querySelector('.menu-button-2');
    const navMenu = document.querySelector('.nav-menu-3');

    if (menuBtn && navMenu) {
        menuBtn.addEventListener('click', () => {
            if (navMenu.style.display === 'flex') {
                navMenu.style.display = 'none';
            } else {
                navMenu.style.display = 'flex';
                navMenu.style.flexDirection = 'column';
                navMenu.style.position = 'absolute';
                navMenu.style.top = '80px';
                navMenu.style.left = '0';
                navMenu.style.width = '100%';
                navMenu.style.background = '#fff';
                navMenu.style.padding = '20px 0';
                navMenu.style.boxShadow = '0 5px 10px rgba(0,0,0,0.1)';
            }
        });
    }

    // --- 【追加】汎用パーツローダー ---
    // data-load="parts/ファイル名.html" と書くだけで自動的に読み込まれます
    const loadTargets = document.querySelectorAll('[data-load]');

    loadTargets.forEach(target => {
        const url = target.getAttribute('data-load');
        if (url) {
            fetch(url)
                .then(res => {
                    if (!res.ok) throw new Error('Load failed');
                    return res.text();
                })
                .then(html => {
                    target.innerHTML = html;
                })
                .catch(err => {
                    console.error(url + ' の読み込みに失敗:', err);
                });
        }
    });
});