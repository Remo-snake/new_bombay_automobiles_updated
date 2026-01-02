<script>
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("show-side-navigation1");
    const openBtn = document.getElementById("sidebar-open-btn");
    const closeBtn = sidebar.querySelector('[data-close="show-side-navigation1"]');

    if (!sidebar) return;

    // OPEN sidebar
    if (openBtn) {
        openBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            sidebar.classList.add("sidebar-open");
        });
    }

    // CLOSE sidebar (✖ button)
    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            sidebar.classList.remove("sidebar-open");
        });
    }

    // CLOSE when clicking outside (mobile only)
    document.addEventListener("click", function (e) {
        if (
            window.innerWidth <= 768 &&
            sidebar.classList.contains("sidebar-open") &&
            !sidebar.contains(e.target) &&
            !openBtn.contains(e.target)
        ) {
            sidebar.classList.remove("sidebar-open");
        }
    });
});
</script>
