var hover = false;
var active = false;

document.getElementById("changeSite").onfocus = function () {
    document.getElementById("sites").style.display = "block";
    active = true;
};
document.getElementById("changeSite").onblur = function () {
    if (!hover) document.getElementById("sites").style.display = "none";
    active = false;
};
document.getElementById("sites").onmouseover = function () {
    document.getElementById("sites").style.display = "block";
    hover = true;
};
document.getElementById("sites").onmouseout = function () {
    if (!active) document.getElementById("sites").style.display = "none";
    hover = false;
};

function loadCharts(viewId){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/ajax.json?viewId=' + viewId, true);
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 0;
        if (this.status != 200) {
            // обработать ошибку
            alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался'));
        }
        else {
            list = JSON.parse(xhr.responseText);
            for (var i = 0; i < list.length; i++){
                createChart(list[i])
            }
        }
        return 0;
    };
    xhr.send();
}

function createChart(chartData) {
    data = chartData['data'];
    var section = document.createElement('section');
    var canvas = document.createElement('canvas');
    section.appendChild(canvas);
    section.setAttribute("id", "section");
    article.appendChild(section);
    section.style.height = chartData['height']+'px';
    section.style.width = chartData['width']+'px';
    var myChart = new Chart(canvas, data);
}