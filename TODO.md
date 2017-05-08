- Add an "`ls` mode" for stat'ing all of the entries in a given directory?
    - Implement this as a separate/alternate entry point?
- Add a command for outputting the results of `os.statvfs` as JSON?
- Add a function for converting just the return value of `os.stat` to a pretty
  `dict`?

- Include unknown `stat` attributes in output
- Include a "basename" field?
- Use `stat` module to deconstruct flags
- Display nanosecond timestamps in ISO format (with full precision) ?
- Display nanosecond timestamps as part of the non-nanosecond timestamps?
- Make `--human-names` use human names for the mode bitfields as well
- Add an option for displaying the values of the `stat` dict verbatim instead
  of formatting them?
- Decompose device numbers (both `st_dev` and `st_rdev`) into major & minor
  values with `os.major` and `os.minor`
- Rename `-H` to `-h` (without interferring with `--help`) and make `-H` the
  negation of `-P`

- Fill in classifiers & keywords in `setup.py`
- Write docstrings and `--help` output

- Support more file attributes:
    - Include ACLs
        - Use pylibacl <http://pylibacl.k1024.org>?
    - Include extended attributes
        - Use the `os` module's `*xattr` functions (Linux only)
        - Use xattr <https://github.com/xattr/xattr>
        - Also support pyxattr <http://pyxattr.k1024.org>?
    - Include SELinux properties?
    - Include capabilities?
