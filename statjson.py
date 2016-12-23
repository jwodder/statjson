#!/usr/bin/python
import argparse
from   base64      import b64encode
from   collections import OrderedDict, defaultdict
from   datetime    import datetime
import grp
import json
import os
import os.path
import pwd
import stat
import sys
import time

fsenc = sys.getfilesystemencoding()
if 'ascii' in fsenc.lower():
    # That can't be right.
    fsenc = 'utf-8'

extra_fields = [
    # Linux:
    ('st_blocks', 'blocks'),
    ('st_blksize', 'block_size'),
    ('st_rdev', 'rdev'),  # "type of device if an inode device"/"device ID (if special file)"
    ('st_flags', 'flags'),
    # FreeBSD:
    ('st_gen', 'generation'),  # file generation number
    ('st_birthtime', 'creation_time'),
    # RISCOS:
    ('st_ftype', 'ftype'),
    ('st_attrs', 'attributes'),
    ('st_obtype', 'object_type'),
    # Mac OS:
    ('st_rsize', 'real_size'),
    ('st_creator', 'creator'),
    ('st_type', 'st_type'),
    # Windows:
    ('st_file_attributes', 'file_attributes'),
]

file_types = defaultdict(lambda: ('?', 'unknown'), {
    stat.S_IFBLK:  ('b', 'block'),
    stat.S_IFCHR:  ('c', 'character'),
    stat.S_IFDIR:  ('d', 'directory'),
    stat.S_IFIFO:  ('p', 'FIFO'),
    stat.S_IFLNK:  ('l', 'symlink'),
    stat.S_IFREG:  ('-', 'regular'),
    stat.S_IFSOCK: ('s', 'socket'),
})

if getattr(stat, 'S_IFDOOR', 0) != 0:
    file_types[stat.S_IFDOOR] = ('D', 'door')
if getattr(stat, 'S_IFPORT', 0) != 0:
    file_types[stat.S_IFPORT] = ('P', 'event_port')
if getattr(stat, 'S_IFWHT', 0) != 0:
    file_types[stat.S_IFWHT] = ('w', 'whiteout')

def strmode(mode):
    # cf. BSD's `strmode(3)`
    # also cf. Python 3.3+'s `stat.filemode`
    return file_types[stat.S_IFMT(mode)][0] \
            + ('r' if mode & stat.S_IRUSR else '-') \
            + ('w' if mode & stat.S_IWUSR else '-') \
            + ('Ss' if mode&stat.S_ISUID else '-x')[bool(mode&stat.S_IXUSR)] \
            + ('r' if mode & stat.S_IRGRP else '-') \
            + ('w' if mode & stat.S_IWGRP else '-') \
            + ('Ss' if mode&stat.S_ISGID else '-x')[bool(mode&stat.S_IXGRP)] \
            + ('r' if mode & stat.S_IROTH else '-') \
            + ('w' if mode & stat.S_IWOTH else '-') \
            + ('Tt' if mode&stat.S_ISVTX else '-x')[bool(mode&stat.S_IXOTH)] \
            + ' '
            ### TODO: Set the last character as follows:
            # extended attributes -> '@' (Mac OS X)
            # security context, no ACLs -> '.' (GNU ls)
            # ACLs -> '+'
            # none of the above: ' '

def iso8601(secs):
    try:
        from dateutil.tz import tzlocal
    except ImportError:
        stamp = datetime.fromtimestamp(secs).isoformat()
        local = time.localtime(secs)
        offset = time.altzone if local.tm_isdst else time.timezone
        if offset <= 0:
            stamp += '+'
            offset *= -1
        else:
            stamp += '-'
        stamp += '{:02}:{:02}'.format(*divmod(offset // 60, 60))
        return stamp
    else:
        return datetime.fromtimestamp(secs, tzlocal()).isoformat()

def about_time(secs, nanosecs):
    about = OrderedDict()
    about["seconds"] = secs
    if nanosecs is not None:
        about["nanoseconds"] = nanosecs
    about["iso8601"] = iso8601(secs)
    return about

def decode(s):
    if isinstance(s, bytes):
        try:
            s = s.decode(fsenc)
        except UnicodeDecodeError:
            return 'base64:' + b64encode(s)
    if s.startswith('base64:'):
        return 'base64:' + b64encode(s.encode(fsenc))
    else:
        return s

def statjson(filename, followlinks=True):
    about = OrderedDict()
    about["filename"] = decode(filename)
    statter = os.stat if followlinks else os.lstat

    try:
        st = statter(filename)
    except Exception as e:
        about["success"] = False
        about["error"] = OrderedDict([
            ("class", e.__class__.__name__),
            ("message", str(e)),
        ])
        return about

    about["success"] = True
    about["followed_symlink"] = followlinks and os.path.islink(filename)
    about["filetype"] = file_types[stat.S_IFMT(st.st_mode)][1]
    if not followlinks and os.path.islink(filename):
        about["target"] = decode(os.readlink(filename))

    about["mode"] = OrderedDict()
    about["mode"]["integer"] = st.st_mode
    about["mode"]["octal"] = '0{0:0o}'.format(st.st_mode)
    about["mode"]["string"] = strmode(st.st_mode)

    about["size"] = st.st_size
    about["inode"] = st.st_ino
    about["device"] = st.st_dev
    about["links"] = st.st_nlink

    about["owner"] = OrderedDict()
    about["owner"]["uid"] = st.st_uid
    try:
        about["owner"]["name"] = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        about["owner"]["name"] = None

    about["group"] = OrderedDict()
    about["group"]["gid"] = st.st_gid
    try:
        about["group"]["name"] = grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        about["group"]["name"] = None

    about["atime"] = about_time(st.st_atime, getattr(st, 'st_atime_ns', None))
    about["mtime"] = about_time(st.st_mtime, getattr(st, 'st_mtime_ns', None))
    about["ctime"] = about_time(st.st_ctime, getattr(st, 'st_ctime_ns', None))

    for attr, name in extra_fields:
        try:
            about[name] = getattr(st, attr)
        except AttributeError:
            pass

    return about

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--no-dereference', action='store_true')
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    stats = [statjson(f, not args.no_dereference) for f in args.file]
    print(json.dumps(stats, indent=4, separators=(',', ': ')))
    sys.exit(0 if all(st["success"] for st in stats) else 1)

if __name__ == '__main__':
    main()
