from xmlrpc.server import  SimpleXMLRPCServer
import socketserver
import requests
import sys

class Crawler:
    def get(self,user,url,params=None,headers=None):
        try:
            if user=='username':
                r=requests.get(url,params=params,headers=headers)
                return r.text
            else:
                return ''
        except Exception as e:
            return e
    def post(self,user,url,data=None,headers=None):
        try:
            if user=='username':
                r=requests.post(url,data=data,headers=headers)
                return r.text
            else:
                return ''
        except Exception as e:
            return e

if __name__=='__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    class RPCThreading(socketserver.ThreadingMixIn,SimpleXMLRPCServer):
        pass
    crawler_object=Crawler()
    server=RPCThreading((ip,int(port)))
    server.register_instance(crawler_object)
    print("Listening")
    server.serve_forever()