let categories = document.querySelectorAll(".category");

document.querySelector("#filter select").addEventListener("change", e => {
    categories.forEach(category => {
        if (e.target.value == "Show all" || category.classList.contains(e.target.value.split(" ")[0])) {
            category.style.display = "flex";
        } else {
            category.style.display = "none";
        }
    });
});
