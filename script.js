document.addEventListener('DOMContentLoaded', () => {

    // --- 1. オープニングアニメーション（Loading） ---
    const loading = document.getElementById('loading');

    // 画面読み込みから少し待ってフェードアウト（演出のため2秒確保）
    // 実際は window.onload で制御するが、ローカル環境だと速すぎるためタイマー併用
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (loading) loading.classList.add('is-loaded');
        }, 1500); // 1.5秒後に幕を上げる
    });


    // --- 2. スクロールフェードイン ---
    const fadeElements = document.querySelectorAll('.js-fadein');

    const observerOptions = {
        root: null,
        rootMargin: "0px 0px -50px 0px",
        threshold: 0
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    fadeElements.forEach(element => {
        observer.observe(element);
    });


    // --- 3. ヘッダーのスクロール検知 ---
    const header = document.querySelector('.header');

    window.addEventListener('scroll', () => {
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        }
    });

    // --- 4. Lazy Load Images (Restored) ---
    const lazyImages = document.querySelectorAll('img.lazy-load');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;

                // Swap src
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }

                // On load, fade in
                img.onload = () => {
                    img.style.opacity = 1;
                    img.classList.add('loaded');
                };

                // Also handle cached images
                if (img.complete) {
                    img.style.opacity = 1;
                    img.classList.add('loaded');
                }

                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: "100px 0px" // Load just before they come into view
    });

    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });

});