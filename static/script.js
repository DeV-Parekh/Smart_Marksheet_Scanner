fetch("static/data.json").then((data) => {
    return data.json();
}).then((objectData) => {
    console.log(typeof objectData);
    console.log(objectData);
    let tableData = "";
    objectData.map((values, index) => {
        tableData += `<tr>
        <td><b>${index + 1}</b></td>
        <td>${values.subject}</td>
        <td>${values.marks}</td>
        <tr>`
    });
    document.getElementById("table_body").innerHTML = tableData;
})