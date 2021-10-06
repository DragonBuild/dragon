#!/usr/env/bin python3
import json
import os
import shutil
import sys
import tarfile

from ruyaml import YAML

from urllib import request
from .util import deployable_path


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

    log('installing dragon v1.6.4')
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
        except Exception as ex:
            log(ex)
            log('Potentially ratelimited, attempting fallback by cloning repo (this adds some overhead)')
            os.system(f'git clone https://github.com/dragonbuild/{repo} --depth 1')

    log('Deploying internal configuration')
    os.system(f'rm -rf ./internal')
    shutil.copytree(deployable_path(),
                    dragondir + '/internal')

    try:
        os.mkdir(os.path.expandvars('$HOME/.dragon/toolchain'))
    except FileExistsError:
        pass
    log('Done!')


def get_supporting(api: str, destination: str):
    response: dict = json.load(request.urlopen(api))
    if os.path.exists(f'{destination}/metadata.yml'):
        with open(f'{destination}/metadata.yml', 'r') as fd:
            yaml=YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
            metadata = yaml.load(fd)
            version = metadata['version']
            if version == response['tag_name']:
                log(f'Latest {destination} already installed')
                return
    tar_url = response['tarball_url']

    os.system(f'rm -rf ./{destination}')

    log(f'Updating supporting {destination} v{response["tag_name"]} from {tar_url} ...')
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
