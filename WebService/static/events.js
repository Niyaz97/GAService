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