#!/usr/env/bin python3
import json
import os
import shutil
import sys
import tarfile

from urllib import request
from dragontools.util import deployable_path


dragondir = ''


def log(s: str, end: str = '\n') -> None:
    print(s, file=sys.stderr, end=end)
    sys.stderr.flush()


def get_input(prompt: str, default: str) -> str:
    log(f'{prompt} ({default})', end='\n> ')
    ret = input()
    return ret if ret.strip() else default


def setup_wizard():
    if os.environ.get('foo'):
        exit(0)

    columns = int(os.popen('stty size', 'r').read().split()[1])

    log('DragonBuild setup utility'.center(columns))
    log('========================='.center(columns), end='\n\n')
    log('For basic users, press return for default options')

    dragondir = os.path.expandvars(
        get_input('Dragonbuild directory', '$HOME/.dragon/')
    )
    if dragondir != os.path.expandvars('$HOME/.dragon/'):
        log('Be sure to set $DRAGONDIR in your shell profile!')

    try:
        os.mkdir(os.path.expandvars(dragondir))
    except FileExistsError:
        pass

    os.chdir(dragondir)

    for repo in ('lib', 'include', 'frameworks', 'vendor', 'sdks'):
        get_supporting(
            f'https://api.github.com/repos/DragonBuild/{repo}/releases/latest',
            repo
        )

    log('Deploying internal configuration')
    shutil.copytree(deployable_path(),
                    dragondir + '/internal')
    log('Done!')


def get_supporting(api: str, destination: str):
    response: dict = json.load(request.urlopen(api))
    tar_url = response['tarball_url']

    log(f'Dowloading supporting {destination} from {tar_url} ...')
    tar_bytes = request.urlopen(tar_url).read()

    fname = 'tmp.tar.gz'
    with open(fname, 'wb') as f:
        f.write(tar_bytes)

    tar = tarfile.open(fname)
    extracted_name = tar.members[0].name

    log(f'Extracting into {os.path.expandvars(dragondir + destination)}')
    tar.extractall()
    os.rename(extracted_name, destination)
    os.remove(fname)


if __name__ == '__main__':
    setup_wizard()
