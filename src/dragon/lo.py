from ruyaml import YAML
import platform
from urllib import request
import json, os, ssl, sys, tarfile
from tqdm import tqdm
from dragon.util import dprintline, OutputColors, OutputWeight

plat = platform.platform()
host_os = plat.split('-')[0]
host_arch = plat.split('-')[2]

ssl._create_default_https_context = ssl._create_unverified_context

def log(s: str, end: str = '\n') -> None:
    dprintline(OutputColors.Cyan, "llvm-ObjCS", OutputColors.White, OutputWeight.Normal, False, s)


iurl = "https://api.github.com/repos/DragonBuild/llvm-objcs/releases/latest"


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1], ) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def install_from_url(ctx, url: str):
    log(f'Downloading {url}, this may take a moment...')
    fname = os.environ["DRAGON_ROOT_DIR"] + '/tmp.tar.gz'
    download_url(url, fname)
    tar = tarfile.open(fname)

    log(f'Extracting into {os.environ["DRAGON_ROOT_DIR"]}' + '/llvm-objcs')
    try:
        os.makedirs(os.environ["DRAGON_ROOT_DIR"] + '/llvm-objcs')
    except OSError:
        pass
    tar.extractall(os.environ["DRAGON_ROOT_DIR"] + '/llvm-objcs')
    os.remove(fname)


def fetch():
    destination = os.environ['DRAGON_ROOT_DIR'] + '/llvm-objcs'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response: dict = json.load(request.urlopen(iurl, context=ctx))
    if os.path.exists(f'{destination}/metadata.yml'):
        with open(f'{destination}/metadata.yml', 'r') as fd:
            yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
            metadata = yaml.load(fd)
            version = metadata['version']
            if version == response['tag_name']:
                log('Latest LLVM-ObjCS build already installed')
                return
    for asset in response['assets']:
        n = asset['name']
        n = n.replace('llvm-objcs-', '').replace('.tar.gz', '')
        op_sys = n.split('-')[0]
        arch = n.split('-')[1]
        if op_sys.lower() == host_os.lower() and arch.lower() == host_arch.lower():
            log(f"Found build for {op_sys}-{arch}, installing")
            install_from_url(ctx, asset['browser_download_url'])
            return

    log(f"Couldn't find a build for {host_os}-{host_arch}")


# tag format: llvm-objcs-0.0.1-llvm-17.0.0
if __name__ == "__main__":
    if 'setup' in sys.argv[1] or 'update' in sys.argv[1]:
        fetch()
