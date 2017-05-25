var hover = false;
var active = false;
var startDateDiv = true;
var endDateDiv = true;

function getUrlVars() {
    var vars = {};
    //var parts =
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}


function check(id) {
    if (id[0] == 's')
        startDateDiv = (id[2] == 'd');
    else
        endDateDiv = (id[2] == 'd');
    if (id[2] == 'd') {
        id = id[0] + id[1];
        document.getElementById(id + 'd').style.position = 'static';
        document.getElementById(id + 'i').style.position = 'absolute';
    } else {
        id = id[0] + id[1];
        startDateDiv = true;
        document.getElementById(id + 'i').style.position = 'static';
        document.getElementById(id + 'd').style.position = 'absolute';
    }
}

function loadChart(numb){
    var viewId = getUrlVars()["viewId"];
    var xhr = new XMLHttpRequest();
    if (numb == undefined)
        xhr.open("GET", '/ajax.json?viewId='+viewId, true);
    else
        xhr.open("GET", '/ajax.json?viewId='+viewId+'&numb='+numb, true);
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return 0;
        if (this.status != 200) {
            // обработать ошибку
            alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался'));
        }
        else {
            var charts = JSON.parse(xhr.responseText);
            if (numb == undefined)
                for (var i = 0; i < charts.length; i++)
                    createChart(i+1, charts[i])
            else
                createChart(numb, charts[0])
        }
        return 0;
    };
    xhr.send();
}


function createChart(numb, chart) {
    var data = chart['data'];
    var section = document.getElementById('section'+numb);
    var canvas = document.getElementById('canvas'+numb);
    section.style.height = chart['height']+'px';
    section.style.width = chart['width']+'px';
    canvas.setAttribute('height', chart['height']+'px');
    canvas.setAttribute('width', chart['width']+'px');
    var myChart = new Chart(canvas, data);
}

/*function addSite() {
    document.location.href = '/analitic?addSite=' + document.getElementById("changeSite").value;
}*/