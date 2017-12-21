import fullsocket
import hashlib

client = fullsocket.FullSocket()
client.connect(('127.0.0.1', 5000))
bash_history=list()
help_command = '''
ok + <filename> for recv a file
pwd : show current directory
cd + <dir> : move to <dir> (if exist)
list : show file of current dir
q : quit program
help : to show this command            
'''
checked=False
print help_command
try:
    while not checked:
        psw=raw_input('Inserisci pswd: ')
        pswd_send=hashlib.sha224()
        pswd_send.update(psw)
        client.send(pswd_send.digest())
        access=client.recv()
        if access == 'confirmed':
            checked=True
        else:
            print 'Access Denied'


    client.send('pwd')
    directory=client.recv()
    while True:
        x = raw_input(directory+' > ')
        bash_history.append(x)
        if x == 'q':
            client.close()
            break
        elif x[:2] == 'cd':
            client.send(x)
            risp = client.recv()
            if '/' in risp:
                directory=risp
                print risp
            else:
                print risp

        elif x[:2] == 'ok':
            client.send(x)
            confirm = client.recv()
            print confirm
            if confirm[:5] == 'EXIST':
                to_send = raw_input('Confirm download? [s/n]')
                if to_send == 's':
                    client.send('confirmed')
                    with open(x[3:], 'wb') as f:
                        f.write(client.recv())
                else:
                    client.send('aborted')

        elif x == 'help':
            print help_command

        else:
            client.send(x)
            msg_recv = client.recv()
            print msg_recv

except KeyboardInterrupt:
    client.close()
