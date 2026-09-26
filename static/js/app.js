// Simple, clean search and filter for task items
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("taskSearchInput");
    const prioritySelect = document.getElementById("priorityFilterSelect");
    const filterTabs = document.querySelectorAll(".filter-tab-btn");
    const taskCards = document.querySelectorAll(".task-item-card");
    const emptyState = document.getElementById("noFilterResultsState");

    let currentStatus = "all";

    function filterTasks() {
        if (!taskCards.length) return;

        const query = (searchInput ? searchInput.value : "").trim().toLowerCase();
        const selectedPriority = prioritySelect ? prioritySelect.value : "all";
        let count = 0;

        taskCards.forEach((card) => {
            const title = (card.getAttribute("data-title") || "").toLowerCase();
            const desc = (card.getAttribute("data-desc") || "").toLowerCase();
            const status = (card.getAttribute("data-status") || "").toLowerCase();
            const priority = (card.getAttribute("data-priority") || "").toLowerCase();

            const matchQuery = !query || title.includes(query) || desc.includes(query);
            const matchStatus = currentStatus === "all" || status === currentStatus.toLowerCase();
            const matchPriority = selectedPriority === "all" || priority === selectedPriority.toLowerCase();

            if (matchQuery && matchStatus && matchPriority) {
                card.style.display = "";
                count++;
            } else {
                card.style.display = "none";
            }
        });

        if (emptyState) {
            emptyState.style.display = count === 0 && taskCards.length > 0 ? "block" : "none";
        }
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterTasks);
    }

    if (prioritySelect) {
        prioritySelect.addEventListener("change", filterTasks);
    }

    if (filterTabs.length) {
        filterTabs.forEach((tab) => {
            tab.addEventListener("click", () => {
                filterTabs.forEach((t) => t.classList.remove("active", "btn-secondary"));
                filterTabs.forEach((t) => t.classList.add("btn-outline-secondary"));
                tab.classList.remove("btn-outline-secondary");
                tab.classList.add("active", "btn-secondary");

                currentStatus = tab.getAttribute("data-status") || "all";
                filterTasks();
            });
        });
    }
});
