function download( j) {
    setTimeout(() => {
    // for (var ii = j * maxsize; ii < j * maxsize + maxsize; ii++) {
    //     if (ii >= len) {
    //         break;
    //     }
    // content += urls[ii]+"\n";
    // }
    const content = urls.join("\n");
    const file = new Blob([content], { type: "text/plain" });
    var encodedUri = encodeURI(content);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", date + "_" + j + "_urls.txt");

    document.body.appendChild(link);
    link.click();
        if (j < Math.ceil(len / maxsize)) {
            download(j + 1);
        }
    }, 1000);
}
download( 0);