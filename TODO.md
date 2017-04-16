- Add an option for using fields' internal (`st_*`) names instead of
  human-friendly names
    - Do this by default?
- Add an option for including a dict of broken-out boolean permission fields
  (`IXOTH`, `IRUSR`, etc.)
- Add an "`ls` mode" for stat'ing all of the entries in a given directory?
- Add a function for converting just the return value of `os.stat` to a pretty
  `dict`?

- Include unknown `stat` attributes in output
- Include device name?
- Include a "basename" field?
- Use `stat` module to deconstruct flags and `st_file_attributes`
- Display `st_birthtime` using `about_time`

- Fill in classifiers & keywords in `setup.py`
- Write docstrings and `--help` output
- Write a README, put on GitHub, etc.

- Support more file attributes:
    - Include ACLs
        - Use pylibacl <http://pylibacl.k1024.org>?
    - Include extended attributes
        - Use xattr <https://github.com/xattr/xattr>
        - Also support pyxattr <http://pyxattr.k1024.org>?
    - Include SELinux properties?
    - Include capabilities?
