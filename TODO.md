- Include unknown `stat` attributes in output
- Add an option for using fields' internal (`st_*`) names instead of
  human-friendly names
    - Do this by default?
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
- Write a README, put on GitHub, etc.
- Add a function for converting just the return value of `os.stat` to a pretty
  `dict`?
- Include a "basename" field?
