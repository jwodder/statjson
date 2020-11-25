from   collections import defaultdict
import stat

file_types = defaultdict(lambda: 'unknown', {
    stat.S_IFBLK:  'block',
    stat.S_IFCHR:  'character',
    stat.S_IFDIR:  'directory',
    stat.S_IFIFO:  'FIFO',
    stat.S_IFLNK:  'symlink',
    stat.S_IFREG:  'regular',
    stat.S_IFSOCK: 'socket',
})

if getattr(stat, 'S_IFDOOR', 0) != 0:
    file_types[stat.S_IFDOOR] = 'door'
if getattr(stat, 'S_IFPORT', 0) != 0:
    file_types[stat.S_IFPORT] = 'event_port'
if getattr(stat, 'S_IFWHT', 0) != 0:
    file_types[stat.S_IFWHT] = 'whiteout'

def strmode(mode):
    return stat.filemode(mode) + ' '
    ### TODO: Set the last character as follows:
    # extended attributes -> '@' (Mac OS X)
    # security context, no ACLs -> '.' (GNU ls)
    # ACLs -> '+'
    # none of the above: ' '
