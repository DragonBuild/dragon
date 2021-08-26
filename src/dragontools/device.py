#!/usr/bin/env python3

'''

device.py

(c) 2020 kritanta
Please refer to the LICENSE file included with dragon regarding the usage of code herein.

https://dragon.krit.me/
https://github.com/DragonBuild/dragon

'''

import os, sys, yaml
import subprocess
import socket

colors = [["\033[0;31m","\033[0;32m","\033[0;33m","\033[0;34m","\033[0;36m",
"\033[0;37m","\033[0m"],["\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m",
"\033[1;36m","\033[1;37m","\033[0m"]]

def dprintline(col: int, tool: str, textcol: int, bold: int, pusher: int, msg: str):
    print("%s[%s]%s %s%s%s" % (
        colors[1][col], tool, colors[bold][textcol], ">>> " if pusher else "", msg, colors[0][6]), file=sys.stdout)

dbstate = lambda msg: dprintline(1, "Device", 5, 1, 0, msg)
dbwarn = lambda msg: dprintline(2, "Device", 5, 0, 0, msg)
dberror = lambda msg: dprintline(0, "Device", 5, 1, 0, msg)

def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(proc.returncode)
    return proc.returncode  # , std_out, std_err

class Device(object):

    def __init__(self, host: str, port: int, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def as_dict(self):
        return {'ip': self.host, 'port': self.port}

    def test_connection(self):
        # pulled this from a one-liner in the bash script. TODO: expand
        try:
            check = lambda x,y,z: (lambda s: (s.settimeout(z), s.connect((x, int(y))), s.close(), True))(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
            check(socket.gethostbyname(self.host),self.port,self.timeout)
        except:
            return False
        return True

    def test_keybased_auth(self):
        return system(f'ssh -o PasswordAuthentication=no -p {self.port} root@{self.host} 2>/dev/null "true"') == 0

    def run_cmd(self, cmd, quiet=False):
        if cmd == "none": return
        if not quiet:
            if cmd == '':
                dbstate(f'No command entered.')
                return
            dbstate(f'Running "{cmd}" on {self.host}:{self.port}')
        return system(f'ssh -p {self.port} root@{self.host} "{cmd}"')

    def export_ip(self):
        exports = {
            'DRBIP': self.host,
            'DRBPORT': self.port
        }
        for x in exports:
            print(f'export {x}="{exports[x]}"')

    def setup_key_auth(self):
        dbstate('Setting up keybased auth')
        exists = system('stat ~/.ssh/id_rsa') == 0
        if not exists:
            dbstate('Generating Keyfile')
            system("ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y 2>&1 >/dev/null")
        
        # We don't use ssh-copy-id because some systems (bingners bootstrap, etc) don't have it
        dbstate('Copying keyfile')
        success = system(f'cat ~/.ssh/id_rsa.pub | ssh -p {self.port} root@{self.host} "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"')
        if success == 0:
            dbstate('Enabled keybased auth')
        else:
            dberror('Failed')


class DeviceManager(object):

    def __init__(self):
        with open(f'{os.environ["DRAGONDIR"]}/internal/state.yml') as state:
            dragon_state = yaml.safe_load(state)

        self.dragon_state = dragon_state
        devices: list = dragon_state['device']['devices']
        self.devices = []
        for i in devices:
            self.devices.append(Device(i['ip'], i['port']))

        self.current = self.devices[dragon_state['device']['current']]

    def savestate(self):
        with open(f'{os.environ["DRAGONDIR"]}/internal/state.yml', 'w') as state:
            yaml.dump(self.dragon_state, state)
    
    def add_device(self, device: Device):
        self.dragon_state['device']['devices'].append({'ip': device.as_dict()['ip'], 'port': device.as_dict()['port']})
        self.devices.append(device)
        self.dragon_state['device']['current'] = len(self.devices)-1
        self.savestate()
    
    def setup(self):
        '''
        Setup checklist:
        1. Get IP/Port, create a device
        2. Test connection
        3. Check and setup key auth

        '''
        
        dbstate('Enter Device IP or hostname')
        ip = input('>>> ')
        dbstate('enter port (leave empty for 22)')
        port = input('>>> ')

        if port == '':
            port = 22

        port = int(port)

        device = Device(ip, port)

        dbstate('Testing Connection')
        connected = False
        if device.test_connection():
            dbstate('Connected!')
            connected = True
        else:
            dbwarn('Connection failed, add it anyways? (y/n)')
            if 'y' not in input('> ').lower():
                return 
            
        if connected:
            if not device.test_keybased_auth():
                device.setup_key_auth()
        
        self.add_device(device)

# device.py cmd
def main():
    device_manager = DeviceManager()
    if 'setup' in sys.argv[1]:
        try:
            device_manager.setup()
        except KeyboardInterrupt:
            print()
            dbstate('Cancelled')
    if 'run' in sys.argv[1]:
        device_manager.current.run_cmd(' '.join(sys.argv[2:]))
    if 'qr' in sys.argv[1]:
        device_manager.current.run_cmd(' '.join(sys.argv[2:]), quiet=True)
    if 'get' in sys.argv[1]:
        device_manager.current.export_ip()
    if 'test' in sys.argv[1]:
        dbstate('Testing Connection')
        if device_manager.current.test_connection():
            dbstate('Connected!')
            exit(0)
        else:
            dberror('Connection Failed')
            dberror('Error connecting to device, make sure SSH is functioning properly')
            exit(1)


if __name__ == '__main__':
    main()
