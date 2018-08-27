from   collections import namedtuple, OrderedDict
import grp
import os
import pwd
import stat
from   .filetypes  import strmode
from   .time       import about_time

Field = namedtuple('Field', 'attr st_name human_name formatter')

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

def about_flags(flags):
    return OrderedDict(
        (prop, bool(flags & getattr(stat, prop)))
        for prop in 'UF_NODUMP UF_IMMUTABLE UF_APPEND UF_OPAQUE UF_NOUNLINK'
                    ' UF_COMPRESSED UF_HIDDEN SF_ARCHIVED SF_IMMUTABLE'
                    ' SF_APPEND SF_NOUNLINK SF_SNAPSHOT'.split()
    )

def about_device(dev):
    return OrderedDict([
        ("device_id", dev),
        ("major_id", os.major(dev)),
        ("minor_id", os.minor(dev)),
    ])

FIELDS = [
    Field('st_mode',  'st_mode',  'mode',              about_mode),
    Field('st_ino',   'st_ino',   'inode',             identity),
    Field('st_dev',   'st_dev',   'device',            about_device),
    Field('st_nlink', 'st_nlink', 'links',             identity),
    Field('st_uid',   'st_uid',   'user',              about_user),
    Field('st_gid',   'st_gid',   'group',             about_group),
    Field('st_size',  'st_size',  'size',              identity),
    Field('st_atime', 'st_atime', 'access_time',       about_time),
    Field('st_mtime', 'st_mtime', 'modification_time', about_time),
    Field('st_ctime', 'st_ctime', 'change_time',       about_time),

    Field(
        'st_atime_ns',
        ('st_atime', 'nanoseconds'),
        ('access_time', 'nanoseconds'),
        identity,
    ),
    Field(
        'st_mtime_ns',
        ('st_mtime', 'nanoseconds'),
        ('modification_time', 'nanoseconds'),
        identity,
    ),
    Field(
        'st_ctime_ns',
        ('st_ctime', 'nanoseconds'),
        ('change_time', 'nanoseconds'),
        identity,
    ),

    # Linux:
    Field('st_blocks',  'st_blocks',  'blocks',     identity),
    Field('st_blksize', 'st_blksize', 'block_size', identity),
    Field('st_rdev',    'st_rdev',    'rdev',       about_device),
        # "type of device if an inode device" / "device ID (if special file)"
    Field('st_flags',   'st_flags',   'flags',      about_flags),

    # FreeBSD (including Mac OS X):
    Field('st_gen',       'st_gen',       'generation',    identity),
        # file generation number
    Field('st_birthtime', 'st_birthtime', 'creation_time', about_time),

    # st_ftype, st_attrs, st_obtype - RISC OS only; not supported by Python 3
    # st_fstype - Solaris only
    # st_rsize, st_creator, st_type - Mac OS Classic only
    # st_file_attributes - Windows only
]

def stat2dict(st, human_names=False):
    about = OrderedDict()
    for field in FIELDS:
        try:
            value = getattr(st, field.attr)
        except AttributeError:
            continue
        value = field.formatter(value)
        key = field.human_name if human_names else field.st_name
        if isinstance(key, tuple):
            d = about
            for k in key[:-1]:
                d = d[k]
            d[key[-1]] = value
        else:
            about[key] = value
    return about
