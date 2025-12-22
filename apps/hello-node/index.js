const http = require("http");

const PORT = process.env.PORT || 3000;

http.createServer((_, res) => {
  res.end("Hello from MinPaas (Node)");

  setInterval(() => {
    console.log("MinPaas log heartbeat");
}, 2000);
  
}).listen(PORT);
