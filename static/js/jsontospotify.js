document.getElementById('send').onclick = function () {
    var files = document.getElementById('selectJson').files;
    if (files.length !== 1) {
        return false;
    }

    var fr = new FileReader();

    fr.onload = function (e) {
        var result = JSON.parse(e.target.result);
        var formatted = JSON.stringify(result, null, 2);
        $.ajax({
            type: "POST",
            url: "/jsontospotify",
            data: formatted,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: () => {
                document.getElementById("success").hidden = false;
            }
        })
    }

    fr.readAsText(files.item(0));
};