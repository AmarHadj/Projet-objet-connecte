var Connection = require('tedious').Connection;
var Request = require('tedious').Request
var TYPES = require('tedious').TYPES;

module.exports = function (context, myTimer) {

    var _currentData = {};

    var config = {
        userName: 'tp2user',
        password: '!FG456dj1',
        server: 'tp2.mariadb.database.azure.com',
        options: {database: 'azureTp2'}
    };

    var connection = new Connection(config);
    connection.on('connect', function(err) {
        context.log("Connected");
        getPerformance();
    });

    function getPerformance() {

        request = new Request("SELECT * FROM tp2Infos;", function(err) {
        if (err) {
            context.log(err);}
        });

        request.on('row', function(columns) {
            _currentData.temp = columns[0].value;
            _currentData.pourcentageOpening = columns[1].value;
            _currentData.action= columns[2].value;
            _currentData.pourcentageManual = columns[4].value;;
            context.log(_currentData);
        });
        connection.execSql(request);
    }

    context.done();
};