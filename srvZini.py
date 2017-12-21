import fullsocket
import threading
import os
import hashlib

def handle(cnn,addr):
    current_dir = ''
    while True:
        if current_dir == '':
            current_dir = os.getcwd()
        try:
            msg_recv = cnn.recv()
        except RuntimeError:
            cnn.close()
            print 'Socket connection broken'
            break
        print  str(addr)+ ' : ' + msg_recv
        if msg_recv == 'list':
            string = ''
            files = os.listdir(current_dir)
            for i in files:
                string += i + '\n'
            cnn.send(string)

        elif msg_recv == 'pwd':
            cnn.send(current_dir)

        elif msg_recv[:2] == 'cd':
            direct = msg_recv[3:]
            if os.path.exists(direct) and direct!='..':
                current_dir = direct
                cnn.send(current_dir)
            elif direct == '..':
                tmp=list(current_dir.split('/'))
                tmp.pop(-1)
                current_dir=''
                for i in tmp:
                    if i != '':
                        current_dir+=str('/'+i)
                cnn.send(current_dir)
            else:
                cnn.send('Directory doesn\'t exist')

        elif msg_recv[:2] == 'ok':
            file_to_download=current_dir + '/' + msg_recv[3:]
            if os.path.isfile(current_dir+'/'+msg_recv[3:]):
                cnn.send('EXIST '+str(os.path.getsize(file_to_download))+' kb')
                resp = cnn.recv()
                if resp == 'confirmed':
                    with open(current_dir+'/'+msg_recv[3:], 'rb') as f:
                        cnn.send(f.read())
                    print 'Download Completed'
            else:
                cnn.send('DOESN\'T EXIST '+current_dir+'/'+msg_recv[3:])
        else:
            cnn.send('Command unrecognize')

def authentication(cnn):
    psw = hashlib.sha224()
    psw.update('fileServerZini')
    while True:
        pswd_recv = cnn.recv()
        if pswd_recv == psw.digest():
            cnn.send('confirmed')
            break
        else:
            cnn.send('access denied')


print 'Server Started'
srv = fullsocket.FullSocket()
srv.bind(('', 5000))
srv.listen(5)
connlist = list()
while True:
    try:
        cnn, addr = srv.accept()
        cnn = fullsocket.FullSocket(cnn)
        print 'Connection established ' + str(addr)
        authentication(cnn)
        t = threading.Thread(target=handle, args=(cnn,addr))
        connlist.append(t)
        t.start()
    except KeyboardInterrupt:
        srv.close()
        break
