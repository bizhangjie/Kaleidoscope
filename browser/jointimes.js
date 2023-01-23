var fileName = date+"_times.txt";
var content = times.join("\n");
var a = document.createElement("a");
var file = new Blob([content], { type: "text/plain" });
a.href = URL.createObjectURL(file);
a.download = fileName;
a.click();