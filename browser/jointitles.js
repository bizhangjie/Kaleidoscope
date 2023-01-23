var fileName = date+"_titles.txt";
var content = titles.join("\n");
var a = document.createElement("a");
var file = new Blob([content], { type: "text/plain" });
a.href = URL.createObjectURL(file);
a.download = fileName;
a.click();