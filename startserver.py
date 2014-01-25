from http.server import HTTPServer, CGIHTTPRequestHandler
import pylogger

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/"]

port = 9999

httpd = HTTPServer(("", port), Handler)
pylogger.logEvent("information", "Server started.")
print("serving at port", port)
httpd.serve_forever()
