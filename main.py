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
from GameEngine import GameEngine
from MapGenerator import *

clients = []
algoList = []
server = None
counter = 0
GE = None
path = dirname(abspath(__file__)) + '\\' + "algo" + '\\'
replayPath = dirname(abspath(__file__)) + '\\' + "replay" + '\\'
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
        # code2 = self.request.files['code2'][0]
        fname1 = code1['filename']
        # fname2 = code2['filename']
        extn1 = splitext(fname1)[1]
        # extn2 = splitext(fname2)[1]
        
        with open(path + fname1, 'wb') as writeFile:
            writeFile.write(code1['body'])
        # with open(path + fname2, 'wb') as writeFile:
        #     writeFile.write(code2['body'])
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
        global algoList
        incoming_data = json.loads(msg)
        msg_type = incoming_data["type"]
        if(msg_type == 0):
            
            result = None
            fileName = "testtest1.txt"
            with open(replayPath + fileName) as json_data:
                result = json.load(json_data)
            data = {"type": 1, "jsonData": json.dumps(result)}
            self.write_message(data)
        elif(msg_type == 1):
            print("Removed: ", incoming_data["client_id"])
            for i in clients:
                if(i[0] == self):
                    clients.remove(i)
                    break
        elif(msg_type == 2):
            data = {"type": 1, "algoList": get_algo()}
            self.write_message(data)
        elif(msg_type == 3):
            fileName = algoList[0][:-3] + algoList[1][:-3] + '.txt'
            result = None
            if (not fileName in [f for f in listdir(replayPath) if (isfile(join(replayPath, f)) and splitext(f)[1] == '.txt')]):
                result = GE.Start(getMap2(30, 30), algoList)
                with open(replayPath + fileName, 'w+') as outfile:
                    outfile.write(result)
            else:
                with open(replayPath + fileName) as json_data:
                    result = json.load(json_data)
            data = {"type": 1, "jsonData": json.dumps(result)}
            self.write_message(data)

    def on_close(self):
        pass
            
class Simulate(tornado.web.RequestHandler):
    def post(self):
        global algoList
        algo1 = self.get_body_argument("algo1", default=None, strip=False)
        algo2 = self.get_body_argument("algo2", default=None, strip=False)

        
        algoList.append(algo1)
        algoList.append(algo2)
        self.render("client/index.html")

class SkipUpload(tornado.web.RequestHandler):
    def post(self):
        self.render("index2.html")

settings = {
    "static_path": join(dirname(__file__), "client"),}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", Upload),
        (r"/ws", SocketHandler),
        (r"/simulate", Simulate),
        (r"/skipUpload", SkipUpload),
    ], **settings)



if __name__ == "__main__":
    global GE
    GE = GameEngine(30, 30, 2)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()