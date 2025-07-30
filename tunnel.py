# tunnel.py
# نوشته شده توسط OxSecTrack
# مدیریت تونل SSH و ارتباط امن

import paramiko
import threading
import socket
import select

def forward_tunnel(local_port, remote_host, remote_port, transport):
    class SubHandler:
        def __init__(self, chan):
            self.chan = chan
            self.sock = socket.socket()
            try:
                self.sock.connect((remote_host, remote_port))
            except Exception as e:
                print(f"[OxSecTrack] خطا در اتصال سوکت: {e}")
                return
            self._start_forwarding()

        def _start_forwarding(self):
            while True:
                r, _, _ = select.select([self.sock, self.chan], [], [])
                if self.sock in r:
                    data = self.sock.recv(1024)
                    if len(data) == 0:
                        break
                    self.chan.send(data)
                if self.chan in r:
                    data = self.chan.recv(1024)
                    if len(data) == 0:
                        break
                    self.sock.send(data)

    def handler(chan, host, port):
        SubHandler(chan)

    try:
        transport.request_port_forward("localhost", local_port, handler=handler)
        print(f"[OxSecTrack] تونل باز شد: localhost:{local_port} → {remote_host}:{remote_port}")
        while True:
            pass
    except KeyboardInterrupt:
        print("[OxSecTrack] تونل بسته شد توسط کاربر.")
        transport.close()

def create_ssh_tunnel(host, username, password, port, local_port, remote_port, key_file=None):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"[OxSecTrack] اتصال به {host} با یوزر {username} در پورت {port}...")
        if key_file:
            pkey = paramiko.RSAKey.from_private_key_file(key_file)
            client.connect(host, port=port, username=username, pkey=pkey)
        else:
            client.connect(host, port=port, username=username, password=password)

        transport = client.get_transport()
        threading.Thread(target=forward_tunnel, args=(local_port, 'localhost', remote_port, transport)).start()

    except Exception as e:
        print(f"[OxSecTrack] اتصال SSH با خطا مواجه شد: {e}")