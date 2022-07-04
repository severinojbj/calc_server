'''
Created on 18 de abr de 2021

@author: sjbj
'''
import socket



if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 8888))
    s.listen()
#     conn, addr = s.accept()
#     msg = conn.recv(200)
#     print(msg)   
    while True:
        conn, addr = s.accept()
        msg = conn.recv(2048)
        print(msg)
        conn.send(msg)    
    pass