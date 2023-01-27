import SimpleHTTPServer
import SocketServer

from lanelet import Lanelet2Map

map = Lanelet2Map()

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/is_over_lanelet":
            lat = self.headers.get("lat")
            lon = self.headers.get("lon")
            lanelet_id = map.is_over_lanelet(float(lat), float(lon))
            if lanelet_id:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Lanelet ID: {}".format(lanelet_id))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Point is not over a lanelet.")
        else:
            # Handle other requests
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)



def start_server():
    PORT = 34568
    handler = SocketServer.TCPServer(("", PORT), RequestHandler)
    print "serving at port", PORT
    handler.serve_forever()

if __name__ == "__main__":
    start_server()
