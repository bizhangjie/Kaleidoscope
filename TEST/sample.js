var xpath = "/html/body/div[1]/div[2]/div[2]/div/h2";

var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);

var date = element.singleNodeValue.textContent;

var times = [];
var elements = document.querySelectorAll('body .entry .entry-time');
for (var i = 0; i < elements.length; i++) {
    times.push(elements[i].textContent);
}

var titles = [];
var elements = document.querySelectorAll('body .entry .entry-link');
for (var i = 0; i < elements.length; i++) {
    var title = elements[i].textContent;
    //把,替换成","，把"替换成""，这样就可以在csv文件中正常显示了
    title = title.replace(/"/g, '""');
    title = title.replace(/,/g, '","');
    titles.push(title);
}

var urls = [];
var elements = document.querySelectorAll('body .entry .entry-link a');
for (var i = 0; i < elements.length; i++) {
    urls.push(elements[i].getAttribute('href'));
}

var len = urls.length;
var maxsize = 10;
function download( j) {
    setTimeout(() => {
    var csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "url,time,title\n";
    for (var ii = j * maxsize; ii < j * maxsize + maxsize; ii++) {
        if (ii >= len) {
            break;
        }
        csvContent += urls[ii] + "," + times[ii] + "," + titles[ii] + "\n";
        console.log(ii+"," + times[ii] + "," + titles[ii] + "\n");
    }
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", date + "_" + j + ".csv");
    // console.log("download", date+"_" + j + ".csv");

    document.body.appendChild(link);
    link.click();
        if (j < Math.ceil(len / maxsize)) {
            download(j + 1);
        }
    }, 1000);
}

download( 0);
