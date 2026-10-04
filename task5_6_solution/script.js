document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
    initScrollProgress();
    initRippleEffects();
    initCardTilt();
    initAccessibleModal();
    initPortraitModal();
    initCursorLight();
    initPartyMode();
    initClickFlash();
    initNavigationDemolition();
});

function initScrollReveal() {
    const sections = document.querySelectorAll('.reveal-section');
    if (!('IntersectionObserver' in window)) {
        sections.forEach((section) => section.classList.add('is-visible'));
        return;
    }
    const observer = new IntersectionObserver((entries, sectionObserver) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                sectionObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.16 });
    sections.forEach((section) => observer.observe(section));
}

function initScrollProgress() {
    const updateProgress = () => {
        const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollableHeight > 0 ? window.scrollY / scrollableHeight : 0;
        document.body.style.setProperty('--progress-transform', `scaleX(${progress})`);
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
}

function initRippleEffects() {
    document.querySelectorAll('.w3-button').forEach((button) => {
        button.addEventListener('click', (event) => {
            const ripple = document.createElement('span');
            const buttonBounds = button.getBoundingClientRect();
            const size = Math.max(buttonBounds.width, buttonBounds.height);
            ripple.className = 'ripple';
            ripple.style.height = `${size}px`;
            ripple.style.left = `${event.clientX - buttonBounds.left - size / 2}px`;
            ripple.style.top = `${event.clientY - buttonBounds.top - size / 2}px`;
            ripple.style.width = `${size}px`;
            button.appendChild(ripple);
            ripple.addEventListener('animationend', () => ripple.remove());
        });
    });
}

function initCardTilt() {
    document.querySelectorAll('.artist-card, .tour-card').forEach((card) => {
        card.addEventListener('mousemove', (event) => {
            const bounds = card.getBoundingClientRect();
            const rotateX = ((event.clientY - bounds.top) / bounds.height - 0.5) * -5;
            const rotateY = ((event.clientX - bounds.left) / bounds.width - 0.5) * 5;
            card.style.transform = `translateY(-10px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });
}

function initAccessibleModal() {
    const modal = document.getElementById('ticketModal');
    if (!modal) return;
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') modal.style.display = 'none';
    });
}

function initPortraitModal() {
    const modal = document.getElementById('portraitModal');
    const modalImage = document.getElementById('portraitModalImage');
    const caption = document.getElementById('portraitModalCaption');
    const closeButton = modal?.querySelector('.portrait-close');
    if (!modal || !modalImage || !caption || !closeButton) return;

    let activeTrigger = null;
    const closeModal = () => {
        modal.style.display = 'none';
        activeTrigger?.focus();
    };

    document.querySelectorAll('.portrait-trigger').forEach((trigger) => {
        trigger.addEventListener('click', () => {
            const image = trigger.querySelector('img');
            if (!image) return;
            activeTrigger = trigger;
            modalImage.src = image.currentSrc || image.src;
            modalImage.alt = image.alt;
            caption.textContent = trigger.dataset.artist || image.alt;
            modal.style.display = 'flex';
            closeButton.focus();
        });
    });

    closeButton.addEventListener('click', closeModal);
    modal.addEventListener('click', (event) => {
        if (event.target === modal) closeModal();
    });
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && modal.style.display !== 'none') closeModal();
    });
}

function initCursorLight() {
    let frameRequested = false;
    let pointerX = window.innerWidth / 2;
    let pointerY = window.innerHeight / 3;

    document.addEventListener('pointermove', (event) => {
        pointerX = event.clientX;
        pointerY = event.clientY;
        if (frameRequested) return;
        frameRequested = true;
        requestAnimationFrame(() => {
            document.body.style.setProperty('--pointer-x', `${pointerX}px`);
            document.body.style.setProperty('--pointer-y', `${pointerY}px`);
            frameRequested = false;
        });
    }, { passive: true });
}

function initPartyMode() {
    document.addEventListener('dblclick', () => {
        document.body.classList.toggle('party-mode');
        document.body.classList.add('screen-shake');
        window.setTimeout(() => document.body.classList.remove('screen-shake'), 500);
    });
}

function initClickFlash() {
    document.addEventListener('click', (event) => {
        const flash = document.createElement('span');
        flash.className = 'click-flash';
        flash.style.left = `${event.clientX}px`;
        flash.style.top = `${event.clientY}px`;
        document.body.appendChild(flash);
        flash.addEventListener('animationend', () => flash.remove());
    });
}

function initNavigationDemolition() {
    const navigationLinks = document.querySelectorAll('.nav-glass a[href^="#"], #navDemo a[href^="#"]');

    navigationLinks.forEach((link) => {
        link.addEventListener('click', (event) => {
            const targetId = link.getAttribute('href');
            const target = targetId === '#' ? document.body : document.querySelector(targetId);

            if (!target) return;

            event.preventDefault();
            launchNavigationBreak(target, targetId);
        });
    });
}

function launchNavigationBreak(target, targetId) {
    const demolition = document.createElement('div');
    const transitionType = getTransitionType(targetId);
    demolition.className = `navigation-demolition transition-${transitionType}`;
    demolition.setAttribute('aria-hidden', 'true');

    const transitionTitle = document.createElement('strong');
    transitionTitle.className = 'transition-title';
    transitionTitle.textContent = targetId === '#' ? 'REBOOT' : targetId.slice(1).toUpperCase();
    demolition.appendChild(transitionTitle);

    const pieceCount = transitionType === 'pixels' ? 110 : transitionType === 'cubes' ? 42 : transitionType === 'fire' ? 36 : 30;
    for (let index = 0; index < pieceCount; index += 1) {
        const shard = document.createElement('span');
        shard.className = 'demolition-piece';
        shard.style.setProperty('--piece-index', index);
        shard.style.setProperty('--piece-x', `${(index % 8 - 3.5) * 18}vw`);
        shard.style.setProperty('--piece-y', `${(Math.floor(index / 8) - 2) * 20}vh`);
        shard.style.setProperty('--piece-rotate', `${(index % 2 ? 1 : -1) * (18 + index * 7)}deg`);
        shard.style.setProperty('--piece-delay', `${index * (transitionType === 'pixels' ? 3 : 10)}ms`);
        if (transitionType === 'pixels') {
            shard.style.setProperty('--pixel-x', `${(index % 8) * 12.5}%`);
            shard.style.setProperty('--pixel-y', `${Math.floor(index / 8) * 12.5}%`);
        }
        demolition.appendChild(shard);
    }

    document.body.appendChild(demolition);
    document.body.classList.add('navigation-breaking');

    window.setTimeout(() => {
        const top = targetId === '#' ? 0 : target.offsetTop - 56;
        window.scrollTo({ top: Math.max(top, 0), behavior: 'smooth' });
        history.replaceState(null, '', targetId);
        document.body.classList.remove('navigation-breaking');
    }, 680);

    window.setTimeout(() => demolition.remove(), 1550);
}

function getTransitionType(targetId) {
    if (targetId === '#band') return 'shards';
    if (targetId === '#tour') return 'pixels';
    if (targetId === '#contact') return 'cubes';
    return 'fire';
}
