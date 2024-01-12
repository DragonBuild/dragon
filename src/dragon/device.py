#!/usr/bin/env python3

'''

device.py

(c) 2020 cynder
Please refer to the LICENSE file included with dragon regarding the usage of code herein.

https://dragon.cynder.me/
https://github.com/DragonBuild/dragon

'''

import os, sys, yaml, socket
from shared.util import dbstate, dbwarn, dberror
from shared.util import system, system_with_output, system_pipe_output

class DeviceShell:
    @staticmethod
    def launch(device):
        current_directory = "~"
        while True:
            command = input(f'{current_directory} > ')
            if command.startswith('cd'):
                arg = command.split(' ')[-1]
                if arg.startswith('/'):
                    current_directory = arg
                else:
                    current_directory += "/" + arg
            system_pipe_output(f'ssh -p {device.port} root@{device.host} "cd {current_directory}; {command}"')


class Device:
    def __init__(self, host: str, port: int, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def as_dict(self):
        return {'ip': self.host, 'port': self.port}

    def test_connection(self):
        try:
            check = lambda x, y, z: (lambda s: (s.settimeout(z), s.connect((x, int(y))), s.close(), True))(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            check(socket.gethostbyname(self.host), self.port, self.timeout)
        except:
            return False
        return True

    def connection_failure_resolver(self):
        status, stdout, stderr = system_with_output(f'ssh -p {self.port} root@{self.host} "true"')
        print(f'Error Message:\n{stderr}')

    def test_keybased_auth(self):
        return system(f'ssh -o PasswordAuthentication=no -p {self.port} root@{self.host} 2>/dev/null "true"') == 0

    def check_known_hosts_issue(self):
        status, stdout, stderr = system_with_output(f'ssh -p {self.port} root@{self.host} "true"')
        if status == 255 and stderr != "" and "known_hosts" in stderr:
            # sick, there's a bad entry in known hosts
            return False, stderr
        return True, ""

    def run_cmd(self, cmd, quiet=False):
        if cmd == "none":
            return

        if not self.test_connection():
            dberror("Device", f'Could not connect to device at {self.host}:{self.port}')
            if self.host == "localhost" and self.port == 4444:
                dberror("Device", 'To configure a new device, run "dragon s"')
            self.connection_failure_resolver()
            return

        if not quiet:
            if cmd == '':
                dbstate("Device", "Launching Device Shell")
                DeviceShell.launch(self)
                return
            dbstate("Device", f'Running "{cmd}" on {self.host}:{self.port}')
        return system_pipe_output(f'ssh -p {self.port} root@{self.host} "{cmd}"')

    def export_ip(self):
        exports = {
            'DRBIP': self.host,
            'DRBPORT': self.port
        }
        for x in exports:
            print(f'export {x}="{exports[x]}"')

    def setup_key_auth(self):
        dbstate("Device", 'Setting up keybased auth')
        exists = system('stat ~/.ssh/id_rsa') == 0
        if not exists:
            dbstate("Device", 'Generating Keyfile')
            system("ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y 2>&1 >/dev/null")

        # We don't use ssh-copy-id because some systems (Elucubratus, etc) don't have it
        dbstate("Device", 'Copying keyfile')
        success = system(
            f'cat ~/.ssh/id_rsa.pub | ssh -p {self.port} root@{self.host} "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"')
        if success == 0:
            dbstate("Device", 'Enabled keybased auth')
        else:
            dberror("Device", 'Failed')


class DeviceManager(object):

    def __init__(self):
        with open(f'{os.environ["DRAGON_ROOT_DIR"]}/internal/state.yml') as state:
            dragon_state = yaml.safe_load(state)

        self.dragon_state = dragon_state
        devices: list = dragon_state['device']['devices']
        self.devices = []
        for i in devices:
            self.devices.append(Device(i['ip'], i['port']))

        self.current = self.devices[dragon_state['device']['current']]

    def savestate(self):
        with open(f'{os.environ["DRAGON_ROOT_DIR"]}/internal/state.yml', 'w') as state:
            yaml.dump(self.dragon_state, state)

    def add_device(self, device: Device):
        self.dragon_state['device']['devices'].append({'ip': device.as_dict()['ip'], 'port': device.as_dict()['port']})
        self.devices.append(device)
        self.dragon_state['device']['current'] = len(self.devices) - 1
        self.savestate()

    # noinspection PyMethodMayBeStatic
    def resolve_known_hosts_issue(self, stderr):
        known_hosts_line = ""
        file_location = ""
        for line in stderr.split("\n"):
            if 'Offending' in line:
                known_hosts_line = int(line.split('known_hosts:')[-1])
                file_location = line.split(' key in ')[-1].split(":")[0]

        dbwarn("Device", "There is already an entry in the known_hosts file for your system")
        if file_location:
            dbwarn("Device", f'Bad entry: {file_location}:{known_hosts_line}')
            dbwarn("Device", "You will not be able to connect to this device until this is resolved. Remove this line? (y/n)")
            if 'y' in input('> ').lower():
                try:
                    with open(file_location, "r") as infile:
                        lines = infile.readlines()

                    with open(file_location, "w") as outfile:
                        for pos, line in enumerate(lines):
                            pos += 1
                            if pos != known_hosts_line:
                                outfile.write(line)
                            else:
                                print(f'Removed {line}')
                    return True
                except IOError:
                    dberror("Device", "Error reading or writing to file. Please manually remove the line.")
                    return False
                except Exception:
                    dberror("Device", "Unknown error occured.")
                    return False

        dberror("Device", "Could not automatically resolve any information about the error. Please See the following output.")
        print(stderr)
        return False

    def setup(self):
        '''
        Setup checklist:
        1. Get IP/Port, create a device
        2. Test connection
        3. Check and setup key auth

        '''

        dbstate("Device", 'Enter Device IP or hostname')
        ip = input('>>> ')
        dbstate("Device", 'enter port (leave empty for 22)')
        port = input('>>> ')

        if port == '':
            port = 22

        port = int(port)

        device = Device(ip, port)

        dbstate("Device", 'Testing Connection')
        connected = False
        if device.test_connection():
            dbstate("Device", 'Connected!')
            connected = True
        else:
            dbwarn("Device", 'Connection failed, add it anyways? (y/n)')
            if 'y' not in input('> ').lower():
                return

        if connected:
            success, stderr = device.check_known_hosts_issue()
            if not success:
                resolved = True
                while resolved:
                    resolved = self.resolve_known_hosts_issue(stderr)
                    if resolved:
                        success, stderr = device.check_known_hosts_issue()
                        if success:
                            break
                if success:
                    dbstate("Device", "Successfully resolved issue")
                else:
                    dberror("Device", "Could not resolve known_hosts issue.")

            if not device.test_keybased_auth():
                device.setup_key_auth()
            else:
                dbstate("Device", "Keybased auth already configured")

        self.add_device(device)


# device.py cmd
def main():
    device_manager = DeviceManager()
    if 'setup' in sys.argv[1]:
        try:
            device_manager.setup()
        except KeyboardInterrupt:
            print()
            dbstate("Device", 'Cancelled')
    if 'run' in sys.argv[1]:
        device_manager.current.run_cmd(' '.join(sys.argv[2:]))
    if 'qr' in sys.argv[1]:
        device_manager.current.run_cmd(' '.join(sys.argv[2:]), quiet=True)
    if 'get' in sys.argv[1]:
        device_manager.current.export_ip()
    if 'test' in sys.argv[1]:
        dbstate("Device", 'Testing Connection')
        if device_manager.current.test_connection():
            dbstate("Device", 'Connected!')
            exit(0)
        else:
            dberror("Device", 'Connection to device failed')
            dberror("Device", 'Make sure SSH is functioning properly and/or run "dragon s" to configure your device')
            exit(1)


if __name__ == '__main__':
    main()
