# hello.py

def application(environ, start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    return '<h1>Hello, wb!</h1>'


from wsgiref.simple_server import make_server

httpd = make_server('',8180,application)
print("serving HTTP on port 8180...")

httpd.serve_forever()
