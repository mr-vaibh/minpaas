const http = require("http");

const PORT = process.env.PORT || 3000;

http.createServer((_, res) => {
  res.end("Hello from MinPaas (Node)");
}).listen(PORT);
