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
window.onload = function () {
    let xyz = document.querySelectorAll('.model-list > tbody > tr > .col-outcome_result > a');
    let abc = document.querySelectorAll('.model-list > tbody > tr > .col-outcome_result');
    xyz.forEach((result) => {
        if (result.textContent == 'Positive' || result.textContent == 'positive' || result.textContent == 'Pos' || result.textContent == 'pos' || result.textContent == '+' || result.textContent == '+ve') {
            result.style.backgroundColor = "red";
            result.style.color = "white";
            result.style.padding = "10px 25px";
        }
        if (result.textContent == 'NULL' || result.textContent == 'null' || result.textContent == 'Null') {
            result.style.backgroundColor = "#303030";
            result.style.color = "white";
            result.style.padding = "10px 25px";
        }
    })
    abc.forEach((result) => {
        if (result.textContent.trim() == 'Positive' || result.textContent.trim() == 'positive' || result.textContent.trim() == 'Pos' || result.textContent.trim() == 'pos' || result.textContent == '+' || result.textContent == '+ve') {
            result.style.backgroundColor = "red";
            result.style.color = "white";
            result.style.padding = "5px 15px";
        }
        if (result.textContent.trim() == 'NULL' || result.textContent.trim() == 'null' || result.textContent.trim() == 'Null') {
            result.style.backgroundColor = "#303030";
            result.style.color = "white";
            result.style.padding = "5px 15px";
        }
    })
}
function reloadModel(){
if("{{ session.get('model_changed')}} == 'xyz'"){
    location.reload();
}
}