- Add an "`ls` mode" for stat'ing all of the entries in a given directory?
    - Implement this as a separate/alternate entry point?
- Add a function for converting just the return value of `os.stat` to a pretty
  `dict`?

- Include unknown `stat` attributes in output
- Include a "basename" field?
- Add human names for mode and flag bitfields
- Add an option for displaying the values of the `stat` dict verbatim instead
  of formatting them?
- Rename `-H` to `-h` (without interferring with `--help`) and make `-H` the
  negation of `-P`
- Use symbolic names for `filetype` when `--human-names` is not in effect?

- Write docstrings and `--help` output
- Expand README
- Add more tests
- Add "posix" to keywords & repo topics?

- Support more file attributes:
    - Include ACLs
        - Use pylibacl <http://pylibacl.k1024.org>?
    - Include extended attributes
        - Use the `os` module's `*xattr` functions (Linux only)
        - Use xattr <https://github.com/xattr/xattr>
        - Also support pyxattr <http://pyxattr.k1024.org>?
    - Include SELinux properties?
    - Include capabilities?
    - Include pathconf information?
