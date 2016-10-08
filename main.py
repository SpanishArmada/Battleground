import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from random import randint
from tornado.ioloop import PeriodicCallback
import uuid, subprocess
from os import listdir
from os.path import isfile, join, dirname, splitext, abspath, split
import imp, importlib

clients = []
server = None
counter = 0
path = dirname(abspath(__file__)) + '\\' + "algo" + '\\'
def load_from_file(filepath, expectedClass):
    class_inst = None

    mod_name,file_ext = splitext(split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expectedClass):
        class_inst = getattr(py_mod, expectedClass)()

    return class_inst

def get_algo():
    onlyfiles = [f for f in listdir(path) if (isfile(join(path, f)) and splitext(f)[1] == '.py')]
    return onlyfiles

class Upload(tornado.web.RequestHandler):
    global clients
    def post(self):
        code1 = self.request.files['code1'][0]
        code2 = self.request.files['code2'][0]
        fname1 = code1['filename']
        fname2 = code2['filename']
        extn1 = splitext(fname1)[1]
        extn2 = splitext(fname2)[1]
        # if want to use random file name
        # cname = str(uuid.uuid4()) + extn
        
        with open(path + fname1, 'wb') as writeFile:
            writeFile.write(code1['body'])
        with open(path + fname2, 'wb') as writeFile:
            writeFile.write(code2['body'])
        self.render("index2.html")
        


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index1.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    """
        Type:
            0 - connection established, provides player's id and initial position
    """
    
    def check_origin(self, origin):
        return True
    def open(self):
        global clients
        global counter
        if(self not in clients):
            clients.append([self, counter])
            counter += 1
        data = {"type": 0, "client_id": counter}
        
        self.write_message(data)


    def on_message(self, msg):
        incoming_data = json.loads(msg)
        msg_type = incoming_data["type"]
        if(msg_type == 0):
            data = {"type": 1}
            self.write_message(data)
        elif(msg_type == 1):
            print("Removed: ", incoming_data["client_id"])
            for i in clients:
                if(i[0] == self):
                    clients.remove(i)
                    break
        elif(msg_type == 2):
            print("INSIDE INDEX 2")
            algoList = get_algo()
            print(algoList)
            data = {"type": 1, "algoList": algoList}
            self.write_message(data)

    def on_close(self):
        pass
            
class Simulate(tornado.web.RequestHandler):
    def post(self):
        algo1 = self.get_body_argument("algo1", default=None, strip=False)
        algo2 = self.get_body_argument("algo2", default=None, strip=False)

        f = load_from_file(path + algo1, algo1[:-3])
        f1 = load_from_file(path + algo2, algo2[:-3])
        print(f.getAction([5, 5]))
        print(f1.getAction([5, 5]))

class SkipUpload(tornado.web.RequestHandler):
    def post(self):
        self.render("index2.html")
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", Upload),
        (r"/ws", SocketHandler),
        (r"/simulate", Simulate),
        (r"/skipUpload", SkipUpload),
    ])

def update_client():
    pass
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()