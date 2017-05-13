import argparse
from   base64      import b64encode
from   collections import OrderedDict
import json
import os
import os.path
import stat
import sys
from   .fields     import FIELDS
from   .filetypes  import file_types

fsenc = sys.getfilesystemencoding()
if 'ascii' in fsenc.lower():
    # That can't be right.
    fsenc = 'utf-8'

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

def statjson(filename, follow_symlinks=True, human_names=False):
    about = OrderedDict()
    about["filename"] = decode(filename)
    try:
        st = os.stat(filename, follow_symlinks=follow_symlinks)
    except Exception as e:
        about["success"] = False
        about["error"] = OrderedDict([
            ("class", e.__class__.__name__),
            ("message", str(e)),
        ])
    else:
        about["success"] = True
        if follow_symlinks:
            about["followed_symlink"] = os.path.islink(filename)
        else:
            about["followed_symlink"] = False
            if os.path.islink(filename):
                about["target"] = decode(os.readlink(filename))
        about["filetype"] = file_types[stat.S_IFMT(st.st_mode)]
        about["realpath"] = decode(os.path.realpath(filename))
        for field in FIELDS:
            key = field.human_name if human_names else field.st_name
            try:
                value = getattr(st, field.st_name)
            except AttributeError:
                continue
            about[key] = field.formatter(value)
    return about

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--human-names', action='store_true')
    parser.add_argument('-P', '--no-dereference', action='store_true')
    parser.add_argument('file', nargs='+')
    args = parser.parse_args()
    args.file = [os.fsencode(f) for f in args.file]
    stats = [
        statjson(f, not args.no_dereference, args.human_names)
        for f in args.file
    ]
    print(json.dumps(stats, indent=4))
    sys.exit(0 if all(st["success"] for st in stats) else 1)

if __name__ == '__main__':
    main()
