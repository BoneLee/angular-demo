# coding: utf-8
__author__ = 'bone'

import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import simplejson as json
import tornado.escape
import tornado.gen

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_json_headers(self):
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.set_header("Content-type", "application/json")

        # You could also add 'GET' here, or any other HTTP methods
        # self.add_header('Access-Control-Request-Method', 'POST')

        # This is needed because Sencha sends the 'X-Requested-With' by default
        # self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')

class MainHandler(BaseHandler):
    def get(self):
        self.set_json_headers()
        self.write(json.dumps({
"records": [{
    "Name" : "Ernst Handel",
    "City" : "Graz",
    "Country" : "Austria"
  }, {
    "Name" : "FISSA Fabrica Inter. Salchichas S.A.",
    "City" : "Madrid",
    "Country" : "Spain"
  }, {
    "Name" : "Laughing Bacchus Wine Cellars",
    "City" : "Vancouver",
    "Country" : "Canada"
  }, {
    "Name" : "Magazzini Alimentari Riuniti",
    "City" : "Bergamo",
    "Country" : "Italy"
  }, {
    "Name" : "North/South",
    "City" : "London",
    "Country" : u"中国"
  },]}))


# class ViewHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         name = tornado.escape.xhtml_escape(self.current_user)
#         self.write("It is you to view: " + name)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            # (r"/json", ViewHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login",
            debug=True, # TODO REMOVE
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the DB across all handlers


from tornado.options import define,options,parse_command_line
define('port',default=9999, help='run on the port', type=int)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
