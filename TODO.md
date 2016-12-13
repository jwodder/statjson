- Add an option for just outputting the `stat` structure directly as a dict?
- Include unknown `stat` attributes in output
- Use the `st_*` names for all fields?
- Include device name?
- Use `stat` module to deconstruct flags and `st_file_attributes`
- Include ACLs
    - Use pylibacl <http://pylibacl.k1024.org>?
- Include extended attributes
    - Use xattr <https://github.com/xattr/xattr>
    - Also support pyxattr <http://pyxattr.k1024.org>?
- Include SELinux properties?
- Include capabilities?
- Add an option for including a dict of broken-out boolean permission fields
  (`IXOTH`, `IRUSR`, etc.)
- Add an "`ls` mode" for stat'ing all of the entries in a given directory?
- Add an option for outputting a stream of dicts instead of an array?
- Display `st_birthtime` using `about_time`
- Add a `setup.py` file
- Add a function for converting just the return value of `os.stat` to a pretty
  `dict`
- Add a field containing the full canonical (i.e., with all symlinks resolved)
  path to the file?
- Switch to Python 3?
