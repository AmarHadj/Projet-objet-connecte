const WebSocket = require("ws")
const wss = new WebSocket.Server({port : 8085});
const {createPool} = require('mysql')
wss.on("connection",ws =>{

    const pool = createPool({
        host: "tp2.mariadb.database.azure.com", 
        user: "tp2user@tp2", 
        password: "!FG456dj1",
        database: "azureTp2", 
        port: 3306   
    })
    
    pool.query('select * from graphtable', (err, res) =>{
        ws.send(String(typeof res));
    })
});


