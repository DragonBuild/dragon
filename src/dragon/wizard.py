#!/usr/bin/env python3

import json, os, shutil, ssl, sys, tarfile
from ruyaml import YAML
from urllib import request
from .util import deployable_path


def log(s: str, end: str = '\n') -> None:
    print(s, file=sys.stderr, end=end)
    sys.stderr.flush()


def get_input(prompt: str, default: str) -> str:
    log(f'{prompt} ({default})', end='\n> ')
    ret = input()
    return ret if ret.strip() else default


def setup_wizard():
    log(f'installing dragon v{os.environ["DRAGON_VERS"]}')
    log('=========================', end='\n\n')
    dragon_root_dir = os.environ['DRAGON_ROOT_DIR']
    try:
        os.mkdir(dragon_root_dir)
    except FileExistsError:
        pass

    os.chdir(dragon_root_dir)

    for repo in ('lib', 'include', 'frameworks', 'vendor', 'sdks', 'src'):
        try:
            get_supporting(
                f'https://api.github.com/repos/DragonBuild/{repo}/releases/latest',
                repo
            )
        except Exception as ex:
            log(ex)
            log('Potentially ratelimited, attempting fallback by cloning repo (this adds some overhead)')
            if os.path.isdir(f'{repo}') and os.path.isdir(f'{repo}/.git'):
                os.chdir(f'{repo}')
                os.system('git pull origin $(git rev-parse --abbrev-ref HEAD)')
                os.chdir(dragon_root_dir)
            else:
                os.system(f'git clone --depth=1 https://github.com/dragonbuild/{repo}')

    log('Deploying internal configuration')
    try:
        shutil.rmtree(f'./internal')
    except FileNotFoundError:
        pass
    shutil.copytree(deployable_path(), dragon_root_dir + '/internal')

    try:
        os.mkdir(dragon_root_dir + '/toolchain')
    except FileExistsError:
        pass
    log('Done!')


def get_supporting(api: str, destination: str):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # python doesn't bundle certs on macOS, so we have to disable SSL :)
    response: dict = json.load(request.urlopen(api, context=ctx))
    if os.path.exists(f'{destination}/metadata.yml'):
        with open(f'{destination}/metadata.yml', 'r') as fd:
            yaml=YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
            metadata = yaml.load(fd)
            version = metadata['version']
            if version == response['tag_name']:
                log(f'Latest {destination} already installed')
                return
    tar_url = response['tarball_url']

    try:
        shutil.rmtree(f'./{destination}')
    except FileNotFoundError:
        pass

    log(f'Updating supporting {destination} v{response["tag_name"]} from {tar_url} ...')
    tar_bytes = request.urlopen(tar_url, context=ctx).read()

    fname = 'tmp.tar.gz'
    with open(fname, 'wb') as f:
        f.write(tar_bytes)

    tar = tarfile.open(fname)
    extracted_name = tar.members[0].name

    log(f'Extracting into {os.environ["DRAGON_ROOT_DIR"] + destination}')
    tar.extractall()
    os.rename(extracted_name, destination)
    os.remove(fname)


if __name__ == '__main__':
    setup_wizard()
    os.system('dragon v')
