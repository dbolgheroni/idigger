/* run only after page is loaded */
$(function() {


/* associate event with the 'Generate' button */
$('#generate-btn').click(function (v) {
    var refdate = $('#refdate').val();

    update_gain(refdate);
});

/* update gain */
var update_gain = function (refdate) {
    $.getJSON("http://localhost:5000/api/v0.1/snapshot/" + refdate, function (response) {
        var gain = $('#gain');

        gain_value = response.gain.toFixed(2);

        if (gain_value >= 0) {
            gain.css("color", "blue");
        } else {
            gain.css("color", "red");
        }

        gain.text(response.gain.toFixed(2) + '%');
    });

    var refdate = $('#refdate').val(refdate);

}

/* update table */
var update_table = function () {
    $.getJSON("http://localhost:5000/api/v0.1/stock/all", function (response) {
        /* push stocks to an array */
        var stocks = [];
        for (var s in response) {
            stocks.push(response[s]);
        }

        /* array.sort(comparefn) takes as an argument a function used to
         * sort properly. Original sort only sorts String correctly.
         * 
         * This procedure is described at the Douglas Crockford book
         * "JavaScript: The Good Parts". */
        var by = function (name, minor) {
            return function (o, p) {
                var a, b;

                if (o && p && typeof o === 'object' && typeof p === 'object') {
                    a = o[name];
                    b = p[name];
                    if (a === b) {
                        return typeof minor === 'function' ? minor(o, p) : 0;
                    }
                    if (typeof a === typeof b) {
                        return a < b ? -1 : 1;
                    }
                    return typeof a < typeof b ? -1 : 1;
                } else {
                    throw {
                        name: 'error',
                        message: 'Expected an object when sorting by ' + name
                    };
                }
            };
        };

        stocks.sort(by('gb_eyroc_order', by('code')));

        /* create table */
        var table = $('<table></table>');
        table.prop('border', '1');

        var hdr = $('<tr></tr>');
        hdr.append('<th>Code</th>');
        hdr.append('<th>EY</th>');
        hdr.append('<th>ROC</th>');
        hdr.append('<th>PE</th>');
        hdr.append('<th>ROE</th>');
        table.append(hdr);

        for (i = 0; i < stocks.length; i += 1) {
            var row = $('<tr></tr>');

            if (i < 20) {
                row.addClass("top");
            }

            row.append('<td>' + stocks[i].code + '</td>');
            row.append('<td>' + stocks[i].ey + '</td>');
            row.append('<td>' + stocks[i].roc + '</td>');
            row.append('<td>' + stocks[i].pe + '</td>');
            row.append('<td>' + stocks[i].roe + '</td>');

            table.append(row);
        }

        $('#gb_table').append(table);
    });
}

/* oldest value of the database */
update_gain(20150617);
update_table();

});
