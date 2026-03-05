(function () {
    let activeCancelFormId = null;

    function openCancelModal(regId, eventTitle) {
        activeCancelFormId = `cancel-form-${regId}`;
        const modal = document.getElementById('cancel-modal');
        const eventName = document.getElementById('cancel-event-name');
        if (!modal || !eventName) {
            return;
        }

        eventName.textContent = eventTitle;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.style.overflow = 'hidden';
    }

    function closeCancelModal() {
        const modal = document.getElementById('cancel-modal');
        if (!modal) {
            return;
        }

        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.style.overflow = 'auto';
        activeCancelFormId = null;
    }

    function executeCancellation() {
        if (!activeCancelFormId) {
            return;
        }

        const form = document.getElementById(activeCancelFormId);
        const modalBtn = document.getElementById('confirm-cancel-btn');
        if (!form || !modalBtn) {
            return;
        }

        modalBtn.disabled = true;
        modalBtn.querySelector('.btn-text-container')?.classList.add('hidden');
        modalBtn.querySelector('.btn-spinner-container')?.classList.remove('hidden');
        modalBtn.querySelector('.btn-spinner-container')?.classList.add('flex');

        setTimeout(() => form.submit(), 500);
    }

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('cancel-modal');
        if (modal && event.target === modal) {
            closeCancelModal();
        }
    });

    window.openCancelModal = openCancelModal;
    window.closeCancelModal = closeCancelModal;
    window.executeCancellation = executeCancellation;
})();
