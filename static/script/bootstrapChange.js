// function adjustColumnWidths(table) {
//     const tbody = table.querySelector("tbody");
//     const rows = tbody.querySelectorAll("tr");
//     const firstRow = rows[0];
//     const cells = firstRow.querySelectorAll("td");

//     for (let i = 0; i < cells.length; i++) {
//         const maxWidth = Math.max(
//             ...Array.from(rows, (row) =>
//                 row.querySelectorAll("td")[i].getBoundingClientRect().width
//             )
//         );
//         table.querySelectorAll("th, td")[i].style.width = `${maxWidth}px`;
//     }
// }

// const tables = document.querySelectorAll(".model-list");
// tables.forEach((table) => {
//     adjustColumnWidths(table);
// });