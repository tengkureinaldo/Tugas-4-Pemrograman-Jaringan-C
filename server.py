import socket
import threading
import os

def Mulai(c,sock,addr):   
    sock.send(b"Kuberi 1 permintaan")
    Todo = sock.recv(1024).decode()
    if Todo == "Upload":
        print(str(addr) + " Uploading")
        UploadingThread = threading.Thread(target=Uploader,args=(c,c,))
        UploadingThread.start()
    if Todo == "Delete":
        DeleterThread = threading.Thread(target=Deleter,args=(c,))
        DeleterThread.start()

        
def Deleter(s):
    print("<",str(s),"> Deleting")
    List = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    FilePath = dir_path
    List.append(os.listdir(FilePath))
    simpan = str(List)
    s.send(simpan.encode())
    Filename = s.recv(1024).decode()
    if os.path.isfile(Filename):
        s.send(b"File Found")
        data = s.recv(1024).decode()
        if data == 'Yes':
            os.remove(Filename)
            print("<",str(s),"> Confirmed Deleting of: ",Filename)
        if data == 'No':
            print("<",str(s),"> Cancelled Deleting of: ",Filename)
    else:
        s.send(b"File 404")

def Uploader(c,s):
    filename = s.recv(1024).decode()
    filesize = s.recv(1024)
    strings = str(filesize, 'utf8')
    ukuranfile = int(strings)
    f = open(filename,'wb')
    totalRecv = 0
    while totalRecv < ukuranfile:
        FileContent = s.recv(8192)
        totalRecv += len(FileContent)
        f.write(FileContent)
    s.send(b"Upload Complete!")
    print("Download Complete")
    f.close()
    s.close()
    
    
def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(30)
    
    server_address = ('172.19.0.5', 45000)

    s.bind(server_address)
    print("Server Started...")
 
    while True:
        s.listen(3)
        c, addr = s.accept()
        print("Client Connection: <" + str(addr) + ">")
        MulaiThread = threading.Thread(target=Mulai,args=(c,c,addr))
        MulaiThread.start()

        
if __name__ == '__main__':
    Main()
