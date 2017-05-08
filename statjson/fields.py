from   collections import namedtuple, OrderedDict
import grp
import pwd
import stat
from   .filetypes  import strmode
from   .time       import about_time

Field = namedtuple('Field', 'st_name human_name formatter')

def identity(x):
    return x

def about_mode(m):
    return OrderedDict([
        ("integer", m),
        ("octal", '0{0:0o}'.format(m)),
        ("string", strmode(m)),
        ("bits", OrderedDict(
            (prop, bool(m & getattr(stat, prop)))
            for prop in 'S_ISUID S_ISGID S_ISVTX'
                        ' S_IRUSR S_IWUSR S_IXUSR'
                        ' S_IRGRP S_IWGRP S_IXGRP'
                        ' S_IROTH S_IWOTH S_IXOTH'.split()
        ))
    ])

def about_user(uid):
    try:
        name = pwd.getpwuid(uid).pw_name
    except KeyError:
        name = None
    return OrderedDict([('uid', uid), ('name', name)])

def about_group(gid):
    try:
        name = grp.getgrgid(gid).gr_name
    except KeyError:
        name = None
    return OrderedDict([('gid', gid), ('name', name)])

FIELDS = [
    Field('st_mode',  'mode',   about_mode),
    Field('st_size',  'size',   identity),
    Field('st_ino',   'inode',  identity),
    Field('st_dev',   'device', identity),
    Field('st_nlink', 'links',  identity),
    Field('st_uid',   'user',   about_user),
    Field('st_gid',   'group',  about_group),
    Field('st_atime', 'access_time', about_time),
    Field('st_mtime', 'modification_time', about_time),
    Field('st_ctime', 'change_time', about_time),
    Field('st_atime_ns', 'access_time_nano', identity),
    Field('st_mtime_ns', 'modification_time_nano', identity),
    Field('st_ctime_ns', 'change_time_nano', identity),

    # Linux:
    Field('st_blocks', 'blocks', identity),
    Field('st_blksize', 'block_size', identity),
    Field('st_rdev', 'rdev', identity),
        # "type of device if an inode device" / "device ID (if special file)"
    Field('st_flags', 'flags', identity),

    # FreeBSD (including Mac OS X):
    Field('st_gen', 'generation', identity),  # file generation number
    Field('st_birthtime', 'creation_time', about_time),

    # st_ftype, st_attrs, st_obtype - RISC OS only; not supported by Python 3
    # st_rsize, st_creator, st_type - Mac OS Classic only
    # st_file_attributes - Windows only
]
