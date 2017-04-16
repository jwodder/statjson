from   collections import defaultdict
import stat

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
