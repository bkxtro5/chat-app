from http.server import HTTPServer, CGIHTTPRequestHandler
import pylogger
import chatconfig

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/"]

port = chatconfig.port

httpd = HTTPServer(("", port), Handler)
pylogger.logBar()
pylogger.logEvent("information", "Server started.")
print("serving at port", port)
httpd.serve_forever()
