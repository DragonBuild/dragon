

class ArgList(list):
    '''
    Variables with values of type list: their corresponding delims and prefixes
    '''

    # This LIST_KEYS logic needs to be shortened, its horribly repetitive
    # As its now in a seperate file, as well, that's problematic. Maybe it can be moved
    #       into defaults.py?
    LIST_KEYS = {
        'files': ('', ' '),
        'logos_files': ('', ' '),
        'tweak_files': ('', ' '),  # used for legacy compatibility, isn't actually used.
        'archs': ('', '-arch '),  # Also only for legacy, this is handled in a much more complex manner # TODO: BUGGED
        'c_files': ('', ' '),
        'objc_files': ('', ' '),
        'objcxx_files': ('', ' '),
        'cxx_files': ('', ' '),
        'plists': ('', ' '),
        'swift_files': ('', ' '),
        'dlists': ('', ' '),
        'cflags': ('', ' '),
        'ldflags': ('', ' '),
        'codesignflags': ('', ' '),
        'include': ('-I', ' -I'),
        'header_includes': ('-I', ' -I'),
        'macros': ('-D', ' -D'),
        'prefix': ('-include', ' -include'),
        'fw_dirs': ('-F', ' -F'),
        'additional_fw_dirs': ('-F', ' -F'),
        'fwSearch': ('-F', ' -F'),
        'libSearch': ('-L', ' -L'),
        'lib_dirs': ('-L', ' -L'),
        'additional_lib_dirs': ('-L', ' -L'),
        'libs': ('-l', ' -l'),
        'frameworks': ('-framework ', ' -framework '),
        'stage': ('', '; '),
        'stage2': ('', '; '),
        'lopts': ('', ' '),
        'public_headers': ('', ''),
    }

    def __init__(self, values: list, prefix: str = '', delim: str = ' '):
        super().__init__(values)
        self.delim = delim
        self.prefix = prefix

    def __str__(self):
        return self.prefix + self.delim.join(str(s) for s in self)


# Apparently this isn't used?
class BoolFlag:
    '''
    Variables with values of type bool, and their corresponding flag pairs.
    '''

    BOOL_KEYS = {
        'arc': ('-fobjc-arc', ''),
    }

    def __init__(self, value: bool, flagpair: (str, str)):
        self.value = value
        self.true_flag, self.false_flag = flagpair

    def __bool__(self):
        return self.value

    def __str__(self):
        return self.true_flag if self.value else self.false_flag


class ProjectVars(dict):
    '''
    Safe dictionary with default values based on keys
    '''

    def __getitem__(self, key):
        try:
            ret = dict.__getitem__(self, key)
            if isinstance(ret, list) and key in ArgList.LIST_KEYS and ArgList(ret, *(ArgList.LIST_KEYS[key])) != []:
                return ArgList(ret, *(ArgList.LIST_KEYS[key]))
            if isinstance(ret, bool) and key in BoolFlag.BOOL_KEYS:
                return BoolFlag(ret, BoolFlag.BOOL_KEYS[key])
            if isinstance(ret, list) and len(ret) == 0:
                return ''
            return ret
        except KeyError as ex:
            if key in ['test']:
                raise ex
            return ArgList([]) if key in ArgList.LIST_KEYS else ''
