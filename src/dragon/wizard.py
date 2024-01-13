#!/usr/bin/env python3

import os, shutil, sys
from .util import deployable_path


def log(s: str, end: str = '\n') -> None:
    print(s, file=sys.stderr, end=end)
    sys.stderr.flush()


def setup_wizard():
    log(f'installing dragon v{os.environ["DRAGON_VERS"]}')
    log('=========================', end='\n\n')
    dragon_root_dir = os.environ['DRAGON_ROOT_DIR']
    try:
        os.mkdir(dragon_root_dir)
    except FileExistsError:
        pass

    os.chdir(dragon_root_dir)

    for repo in ('lib', 'include', 'frameworks', 'sdks', 'src'):
        if os.path.isdir(repo) and not os.path.isdir(f'{repo}/.git'):
            shutil.rmtree(repo)
            os.system(f'git clone --recursive https://github.com/DragonBuild/{repo}')
        elif os.path.isdir(repo) and os.path.isdir(f'{repo}/.git'):
            os.chdir(repo)
            os.system('git pull origin $(git rev-parse --abbrev-ref HEAD)')
            os.chdir(dragon_root_dir)
        else:
            os.system(f'git clone --recursive https://github.com/DragonBuild/{repo}')

    log('Deploying internal configuration')
    try:
        shutil.rmtree('./internal')
    except FileNotFoundError:
        pass
    shutil.copytree(deployable_path(), dragon_root_dir + '/internal')

    try:
        os.mkdir(dragon_root_dir + '/toolchain')
    except FileExistsError:
        pass
    log('Done!')


if __name__ == '__main__':
    setup_wizard()
    os.system('dragon v')
