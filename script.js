document.addEventListener('DOMContentLoaded', () => {

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
                navMenu.style.top = '60px'; // ヘッダーの高さに合わせる
                navMenu.style.left = '0';
                navMenu.style.width = '100%';
                navMenu.style.background = '#fff';
                navMenu.style.padding = '20px 0';
                navMenu.style.boxShadow = '0 5px 10px rgba(0,0,0,0.1)';
                navMenu.style.zIndex = '1001';
            }
        });
    }

    // --- 汎用パーツローダー（Serviceページのギャラリー読み込みなど） ---
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
                    // ★★★ まる牛 → まるぎゅう 修正パッチ（ここから） ★★★
                    // HTML内の「表示用の文字」だけを安全に書き換えます
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = html;

                    // 1. カードの下に表示される名前を変更
                    const projectNames = tempDiv.querySelectorAll('.project-name');
                    projectNames.forEach(el => {
                        // 空白削除して判定
                        if (el.textContent.replace(/\s+/g, '') === 'まる牛') {
                            el.textContent = 'まるぎゅう';
                        }
                    });

                    // 2. Lightbox（拡大表示時）のタイトルを変更
                    const links = tempDiv.querySelectorAll('a[data-title="まる牛"]');
                    links.forEach(el => {
                        el.setAttribute('data-title', 'まるぎゅう');
                    });

                    // 修正したHTMLを流し込む
                    target.innerHTML = tempDiv.innerHTML;
                    // ★★★ 修正パッチ（ここまで） ★★★


                    // 部品読み込み完了後、URLのハッシュがあればそこへスクロール
                    if (window.location.hash) {
                        const hash = window.location.hash;
                        setTimeout(() => {
                            const targetElement = document.querySelector(hash);
                            if (targetElement) {
                                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        }, 100);
                    }

                    // Lightboxの初期化（動的読み込みのため再設定）
                    if (typeof lightbox !== 'undefined') {
                        lightbox.option({
                            'resizeDuration': 200,
                            'wrapAround': true
                        });
                    }
                })
                .catch(err => {
                    console.error(url + ' の読み込みに失敗:', err);
                    target.innerHTML = '<p style="text-align:center;">現在準備中です。</p>';
                });
        }
    });

    // --- Workページ上部スライドショー ---
    const slides = document.querySelectorAll('.slide-item');
    let currentSlide = 0;
    const slideInterval = 5000; // 切り替え間隔（ミリ秒 = 5秒）

    if (slides.length > 0) {
        // 最初のスライドを表示
        slides[currentSlide].classList.add('active');

        // 自動切り替えタイマー
        setInterval(() => {
            // 現在のスライドを消す
            slides[currentSlide].classList.remove('active');

            // 次のスライド番号（ループ）
            currentSlide = (currentSlide + 1) % slides.length;

            // 次のスライドを表示
            slides[currentSlide].classList.add('active');
        }, slideInterval);
    }

});