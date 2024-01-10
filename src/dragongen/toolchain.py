import os, os.path
import subprocess
import sys


def system_with_output(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    return proc.returncode, std_out, std_err


class Toolchain:
    def __init__(self):
        self.ass = ""
        self.clang = ""
        self.clangpp = ""
        self.ld = ""
        self.codesign = ""
        self.dsym = ""
        self.lipo = ""
        self.tapi = ""

    @classmethod
    def locate_macos_toolchain(cls, use_objcs: bool):
        tc_dir = ""
        if use_objcs:
            tc_dir = os.environ['DRAGON_ROOT_DIR'] + '/llvm-objcs/bin/'
        else:
            stat, xcrun_out, _ = system_with_output('xcrun -f clang')
            tc_dir = ""

            if stat == 0:
                tc_dir = os.path.dirname(xcrun_out) + '/'
            elif os.path.exists('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/'):
                tc_dir = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/'
            elif system_with_output('command -v clang')[0] == 0:
                pass
            else:
                return None

        tc = cls()
        tc.ass = tc_dir + 'clang'
        tc.clang = tc_dir + 'clang'
        tc.clangpp = tc_dir + 'clang++'
        tc.ld = tc_dir + 'clang++'
        tc.codesign = 'ldid'
        tc.dsym = tc_dir + 'dsymutil'
        # FIXME: hardcoded while I wait on a real distribution of llvm-objcs
        if use_objcs:
            tc.lipo = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/lipo'
        else:
            tc.lipo = tc_dir + 'lipo'
        tc.tapi = tc_dir + 'tapi'

        return tc

    @classmethod
    def locate_linux_toolchain(cls, use_objcs: bool):
        tc_dir = ""
        if use_objcs:
            tc_dir = os.environ['DRAGON_ROOT_DIR'] + '/llvm-objcs/bin/'
        elif os.path.exists(os.environ['DRAGON_ROOT_DIR'] + '/toolchain/linux/iphone/bin/'):
            tc_dir = os.environ['DRAGON_ROOT_DIR'] + '/toolchain/linux/iphone/bin/'
        elif system_with_output('command -v clang')[0] == 0:
            pass
        else:
            return None

        tc = cls()
        tc.ass = tc_dir + 'clang'
        tc.clang = tc_dir + 'clang'
        tc.clangpp = tc_dir + 'clang++'
        tc.ld = tc_dir + 'clang++'
        tc.codesign = tc_dir + 'ldid'
        tc.dsym = tc_dir + 'dsymutil'
        tc.lipo = tc_dir + 'lipo'
        tc.tapi = tc_dir + 'tapi'

        return tc


