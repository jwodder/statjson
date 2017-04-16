import argparse
from   base64      import b64encode
from   collections import OrderedDict
import grp
import json
import os
import os.path
import pwd
import stat
import sys
from   .filetypes import file_types, strmode
from   .time      import about_time

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

def decode(s):
    if isinstance(s, bytes):
        try:
            s = s.decode(fsenc)
        except UnicodeDecodeError:
            return 'base64:' + b64encode(s).decode('us-ascii')
    if s.startswith('base64:'):
        return 'base64:' + b64encode(s.encode(fsenc)).decode('us-ascii')
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
    if followlinks:
        about["followed_symlink"] = os.path.islink(filename)
    else:
        about["followed_symlink"] = False
        if os.path.islink(filename):
            about["target"] = decode(os.readlink(filename))
    about["filetype"] = file_types[stat.S_IFMT(st.st_mode)][1]
    about["realpath"] = decode(os.path.realpath(filename))
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
    args.file = [os.fsencode(f) for f in args.file]
    stats = [statjson(f, not args.no_dereference) for f in args.file]
    print(json.dumps(stats, indent=4))
    sys.exit(0 if all(st["success"] for st in stats) else 1)

if __name__ == '__main__':
    main()
