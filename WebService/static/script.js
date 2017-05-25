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

function loadChart(viewId, numb){
    document.getElementById("changeSite").value = url;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/ajax.json?viewId=' + viewId, true);
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 0;
        if (this.status != 200) {
            // обработать ошибку
            alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался'));
        }
        else {
            chart = JSON.parse(xhr.responseText);
            createChart(chart)
        }
        return 0;
    };
    xhr.send();
}

function createChart(chartData) {
    data = chartData['data'];
    var section = document.getElementById('section');
    var canvas = document.getElementById('canvas');
    section.style.height = chartData['height']+'px';
    section.style.width = chartData['width']+'px';
    canvas.setAttribute('height', chartData['height']+'px');
    canvas.setAttribute('width', chartData['width']+'px');
    var myChart = new Chart(canvas, data);
}

function addSite() {
    document.location.href = '/analitic?addSite=' + document.getElementById("changeSite").value;
}