document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById('menuToggle');
    const menuClose = document.getElementById('menuClose');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const mainContent = document.getElementById('mainContent');

    const openSidebar = () => {
        sidebar?.classList.add('open');
        overlay?.classList.add('active');
    };

    const closeSidebar = () => {
        sidebar?.classList.remove('open');
        overlay?.classList.remove('active');
    };

    menuToggle?.addEventListener('click', openSidebar);
    menuClose?.addEventListener('click', closeSidebar);
    overlay?.addEventListener('click', closeSidebar);

    const toggleButtons = document.querySelectorAll('.toggle-details');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const detailsRow = document.getElementById(`details-${button.dataset.id}`);

            if (detailsRow.classList.contains('hidden')) {
                detailsRow.style.maxHeight = `${detailsRow.scrollHeight}px`; 
                detailsRow.classList.remove('hidden');
                detailsRow.classList.add('visible'); 
                button.classList.add('expanded'); 
            } else {
                detailsRow.style.maxHeight = '0px'; 
                detailsRow.classList.add('hidden');
                detailsRow.classList.remove('visible');
                button.classList.remove('expanded'); 
            }
        });
    });
});