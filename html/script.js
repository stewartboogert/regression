document.getElementById("roleFilter").addEventListener("change", function() {
    const selected = this.value.toLowerCase();
    const rows = document.querySelectorAll("#myTable tbody tr");

    rows.forEach(row => {
        const roleCell = row.children[2].textContent.toLowerCase(); // 3rd column
        row.style.display = (!selected || roleCell === selected) ? "" : "none";
    });
});
