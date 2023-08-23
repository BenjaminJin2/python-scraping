var sss = document.getElementsByClassName("navi current");
console.log(sss[0].textContent);
alert("sdf");

var sa = sss[0].textContent + "endl";

var ttt = sa.replace("endl", "\n");

var a = document.createElement("a");
a.href = window.URL.createObjectURL(new Blob([sss[0].textContent], {type: "text/plain"}));
a.download = "demo.txt";
a.click();