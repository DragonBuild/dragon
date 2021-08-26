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

    log('installing dragon v1.5')
    log('=========================', end='\n\n')
    dragondir = os.path.expandvars('$HOME/.dragon/')
    try:
        os.mkdir(os.path.expandvars(dragondir))
    except FileExistsError:
        pass

    os.chdir(dragondir)

    for repo in ('lib', 'include', 'frameworks', 'vendor', 'sdks', 'src'):
        try:
            get_supporting(
                f'https://api.github.com/repos/DragonBuild/{repo}/releases/latest',
                repo
            )
        except: 
            log('Potentially ratelimited, attempting fallback by cloning repo (this adds some overhead)')
            os.system(f'git clone https://github.com/dragonbuild/{repo} --depth 1')

    log('Deploying internal configuration')
    shutil.copytree(deployable_path(),
                    dragondir + '/internal')
                    
    os.mkdir(os.path.expandvars('$HOME/.dragon/toolchain'))
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
    os.system('dragon v')
