(function () {
    const heroContent = document.getElementById('hero-content');
    const mainNav = document.getElementById('main-nav');
    const root = document.documentElement;

    let ticking = false;

    function handleScroll() {
        const scrollY = window.scrollY;
        sessionStorage.setItem('dashboardScrollPos', String(scrollY));

        if (ticking) {
            return;
        }

        ticking = true;
        window.requestAnimationFrame(() => {
            const scale = Math.max(1, 1.2 - (scrollY / 2500));
            root.style.setProperty('--hero-scale', scale);

            if (heroContent) {
                heroContent.style.opacity = String(Math.max(0, 1 - (scrollY / 600)));
            }

            if (mainNav) {
                if (scrollY > 500) {
                    mainNav.classList.remove('nav-hidden');
                    sessionStorage.setItem('visitedBefore', 'true');
                } else if (!sessionStorage.getItem('visitedBefore')) {
                    mainNav.classList.add('nav-hidden');
                }
            }

            ticking = false;
        });
    }

    function restoreScrollState() {
        const rawScroll = sessionStorage.getItem('dashboardScrollPos');
        const savedScrollPos = rawScroll ? parseInt(rawScroll, 10) : 0;
        const previousInlineBehavior = root.style.scrollBehavior;
        root.style.scrollBehavior = 'auto';

        if (savedScrollPos > 0) {
            window.scrollTo(0, savedScrollPos);
        }

        if (sessionStorage.getItem('visitedBefore') === 'true' && mainNav) {
            mainNav.classList.remove('nav-hidden');
        }

        handleScroll();

        window.requestAnimationFrame(() => {
            root.style.scrollBehavior = previousInlineBehavior;
            root.classList.remove('homepage-preload');
            if (heroContent && !window.scrollY) {
                heroContent.style.opacity = '1';
            }
        });
    }

    function initRevealObserver() {
        const revealEls = document.querySelectorAll('.reveal');
        if (!revealEls.length || !('IntersectionObserver' in window)) {
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('active');
                    }
                });
            },
            { threshold: 0.1 }
        );

        revealEls.forEach((el) => observer.observe(el));
    }

    window.addEventListener('scroll', handleScroll, { passive: true });

    window.addEventListener('pagehide', () => {
        sessionStorage.setItem('dashboardScrollPos', String(window.scrollY));
    });

    window.addEventListener('pageshow', (event) => {
        if (event.persisted || performance.getEntriesByType('navigation')[0]?.type === 'back_forward') {
            restoreScrollState();
        }
    });

    restoreScrollState();

    document.addEventListener('DOMContentLoaded', () => {
        initRevealObserver();
    });
})();
