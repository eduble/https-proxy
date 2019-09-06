#!/usr/bin/env python3
import socket, ssl, select, conf

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('', conf.HTTPS_PORT))
sock.listen(5)
ssock = context.wrap_socket(sock, server_side=True)

monitored = [ ssock ]
mirrored = {}

while True:
    r, w, e = select.select(monitored, [], [])
    if len(r) == 0:
        break
    if r[0] == ssock:
        try:
            sock, addr = ssock.accept()
        except ssl.SSLError as e:
            pass
        mirror_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            mirror_sock.connect(('127.0.0.1', conf.WEBAPP_PORT))
            print('connection forwarded to webapp.')
        except socket.error:
            print('ERROR: could not connect to webapp!')
            mirror_sock.close()
            sock.close()
            continue
        sock.setblocking(0)
        mirror_sock.setblocking(0)
        mirrored[sock] = mirror_sock
        mirrored[mirror_sock] = sock
        monitored.append(sock)
        monitored.append(mirror_sock)
    else:
        sock = r[0]
        mirror_sock = mirrored[sock]
        buf = sock.recv(2048)
        if len(buf) == 0:
            sock.close()
            mirror_sock.close()
            monitored.remove(sock)
            monitored.remove(mirror_sock)
            del mirrored[sock]
            del mirrored[mirror_sock]
        else:
            mirror_sock.send(buf)

