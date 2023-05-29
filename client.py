import socket
import threading
import os
import time
import getpass
 
def Mulai(s):
    data = s.recv(2048).decode()
    if data == "Kuberi 1 permintaan":
        message = input(" -> ")
        if message == "Upload":
            s.send(b"Upload")
            print("Uploader Loading")
            Uploader(s)
        if message == "Delete":
            print("Deleter Loading")
            s.send(b"Delete")
            Deleter(s)
        

        
def Deleter(s):
    List = s.recv(2048)
    print(List)
    print("")
    filename = input("File Name? -> ")
    s.send(filename.encode())
    data = s.recv(2048).decode()
    if data == "File Found":
        
        print("File Found")
        print("You sure you wanna delete? ",filename)
        YN = input(" -> ")
        
        if YN == 'Yes':
            print("Deleting File...")
            s.send(b"Yes")
 
        if YN == 'No':
            print("Cancelling...")
            s.send(b"No")
 
    if data == "File 404":
        print("File 404 not found")
 
 
def Uploader(s):
    IsReal = True
    data = "UploaderReady"
    if data == "UploaderReady":
        List = []
        FilePath = dir_path = os.path.dirname(os.path.realpath(__file__))
        List.append(os.listdir(FilePath))
        FileUpload = input("Pick a file? -> ")
        for Item in List:
            if FileUpload == Item:
                IsReal = True 
        if IsReal == True:
            File = open(FileUpload,'rb')
            bytestosend = File.read(1024)
            FileSize = os.path.getsize(FileUpload)
            simpan = str(FileSize)
            s.send(FileUpload.encode())
            s.send(simpan.encode())
            s.send(bytestosend)
            while bytestosend != "":
                bytestosend = File.read(8192)
                s.send(bytestosend)
                print("Processing")
            s.shutdown(socket.SHUT_WR) 
            print(s.recv(1024)) 
            s.close() 
            File.close()
            time.sleep(1.5)
            s.send(b"COMPLETE")
            s.close() 
            print("File Successfully Uploaded")
            time.sleep(2)
            print("    \n    ") * 10
            Main()
 
 
def Main():
    totalRecv = 0
    Connected = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(30)
    server_address = ('172.19.0.5', 45000)
    print("Connecting To Server..")
    s.connect(server_address)
    Mulai(s)
    
    s.close()

    
if __name__ == '__main__':
    Main()
