#!/usr/bin/env python3

import json, os, urllib.request
from packaging.version import Version

if __name__ == '__main__':
    endpoint = "https://pypi.org/pypi/dragon/json"
    # noinspection PyBroadException
    try:
        with urllib.request.urlopen(endpoint, timeout=1) as url:
            data = json.loads(url.read().decode(), strict=False)
        if Version(os.environ['DRAGON_VERS']) < Version(data['info']['version']):
            print('\nAn update is available!\nGrab it with `dragon update`')
        else:
            if 'UCDBG' in os.environ.keys():
                print(f'Remote Version: {data["info"]["version"]} | Local Version: {os.environ["DRAGON_VERS"]}')
    except Exception:
        pass
