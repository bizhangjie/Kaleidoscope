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
    // title = title.replace(/"/g, '""');
    // title = title.replace(/,/g, '","');
    titles.push(title);
}

var urls = [];
var elements = document.querySelectorAll('body .entry .entry-link a');
for (var i = 0; i < elements.length; i++) {
    urls.push(elements[i].getAttribute('href'));
}
var len = urls.length;
var maxsize = 10;


