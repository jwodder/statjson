from   collections     import OrderedDict
from   copy            import copy
import grp
import pwd
from   types           import SimpleNamespace
import pytest
from   statjson.fields import stat2dict

st = SimpleNamespace(
    st_mode     = 0o100644,
    st_ino      = 1185930,
    st_dev      = 64769,
    st_nlink    = 1,
    st_uid      = 1000,
    st_gid      = 1001,
    st_size     = 4102,
    st_atime    = 1535036782.6969066,
    st_mtime    = 1535036783.6969066,
    st_ctime    = 1535036784.6969066,
    st_atime_ns = 1535036782696906483,
    st_mtime_ns = 1535036783696906483,
    st_ctime_ns = 1535036784696906483,
)

st_dict = OrderedDict([
    ("st_mode", OrderedDict([
        ("integer", 33188),
        ("octal", "0100644"),
        ("string", "-rw-r--r-- "),
        ("bits", OrderedDict([
            ("S_ISUID", False),
            ("S_ISGID", False),
            ("S_ISVTX", False),
            ("S_IRUSR", True),
            ("S_IWUSR", True),
            ("S_IXUSR", False),
            ("S_IRGRP", True),
            ("S_IWGRP", False),
            ("S_IXGRP", False),
            ("S_IROTH", True),
            ("S_IWOTH", False),
            ("S_IXOTH", False),
        ])),
    ])),
    ("st_ino", 1185930),
    ("st_dev", OrderedDict([
        ("device_id", 64769),
        ("major_id", 253),
        ("minor_id", 1),
    ])),
    ("st_nlink", 1),
    ("st_uid", OrderedDict([("uid", 1000), ("name", "a_user")])),
    ("st_gid", OrderedDict([("gid", 1001), ("name", "a_grp")])),
    ("st_size", 4102),
    ("st_atime", OrderedDict([
        ("seconds", 1535036782.6969066),
        ("iso8601", "2018-08-23T11:06:22.696907-04:00"),
    ])),
    ("st_mtime", OrderedDict([
        ("seconds", 1535036783.6969066),
        ("iso8601", "2018-08-23T11:06:23.696907-04:00"),
    ])),
    ("st_ctime", OrderedDict([
        ("seconds", 1535036784.6969066),
        ("iso8601", "2018-08-23T11:06:24.696907-04:00"),
    ])),
    ("st_atime_ns", 1535036782696906483),
    ("st_mtime_ns", 1535036783696906483),
    ("st_ctime_ns", 1535036784696906483),
])

st_human_dict = OrderedDict([
    ("mode", OrderedDict([
        ("integer", 33188),
        ("octal", "0100644"),
        ("string", "-rw-r--r-- "),
        ("bits", OrderedDict([
            ("S_ISUID", False),
            ("S_ISGID", False),
            ("S_ISVTX", False),
            ("S_IRUSR", True),
            ("S_IWUSR", True),
            ("S_IXUSR", False),
            ("S_IRGRP", True),
            ("S_IWGRP", False),
            ("S_IXGRP", False),
            ("S_IROTH", True),
            ("S_IWOTH", False),
            ("S_IXOTH", False),
        ])),
    ])),
    ("inode", 1185930),
    ("device", OrderedDict([
        ("device_id", 64769),
        ("major_id", 253),
        ("minor_id", 1),
    ])),
    ("links", 1),
    ("user", OrderedDict([("uid", 1000), ("name", "a_user")])),
    ("group", OrderedDict([("gid", 1001), ("name", "a_grp")])),
    ("size", 4102),
    ("access_time", OrderedDict([
        ("seconds", 1535036782.6969066),
        ("iso8601", "2018-08-23T11:06:22.696907-04:00"),
    ])),
    ("modification_time", OrderedDict([
        ("seconds", 1535036783.6969066),
        ("iso8601", "2018-08-23T11:06:23.696907-04:00"),
    ])),
    ("change_time", OrderedDict([
        ("seconds", 1535036784.6969066),
        ("iso8601", "2018-08-23T11:06:24.696907-04:00"),
    ])),
    ("access_time_nano", 1535036782696906483),
    ("modification_time_nano", 1535036783696906483),
    ("change_time_nano", 1535036784696906483),
])

st_linux = copy(st)
st_linux.st_blocks  = 16
st_linux.st_blksize = 4096
st_linux.st_rdev    = 0
st_linux.st_flags   = 0

st_freebsd = copy(st)
st_freebsd.st_gen = 0
st_freebsd.st_birthtime = 1535380109.4635055

@pytest.fixture(autouse=True)
def mock_user_and_group(mocker):
    mocker.patch('pwd.getpwuid', return_value=SimpleNamespace(pw_name='a_user'))
    mocker.patch('grp.getgrgid', return_value=SimpleNamespace(gr_name='a_grp'))
    yield
    pwd.getpwuid.assert_called_once_with(1000)
    grp.getgrgid.assert_called_once_with(1001)

def test_basic():
    assert stat2dict(st) == st_dict

def test_human_names():
    assert stat2dict(st, human_names=True) == st_human_dict

def test_linux():
    st_linux_dict = st_dict.copy()
    st_linux_dict["st_blocks"] = 16
    st_linux_dict["st_blksize"] = 4096
    st_linux_dict["st_rdev"] = OrderedDict([
        ("device_id", 0),
        ("major_id", 0),
        ("minor_id", 0),
    ])
    st_linux_dict["st_flags"] = OrderedDict([
        (k, False)
        for k in 'UF_NODUMP UF_IMMUTABLE UF_APPEND UF_OPAQUE UF_NOUNLINK'
                 ' UF_COMPRESSED UF_HIDDEN SF_ARCHIVED SF_IMMUTABLE'
                 ' SF_APPEND SF_NOUNLINK SF_SNAPSHOT'.split()
    ])
    assert stat2dict(st_linux) == st_linux_dict

def test_linux_human_names():
    st_linux_dict = st_human_dict.copy()
    st_linux_dict["blocks"] = 16
    st_linux_dict["block_size"] = 4096
    st_linux_dict["rdev"] = OrderedDict([
        ("device_id", 0),
        ("major_id", 0),
        ("minor_id", 0),
    ])
    st_linux_dict["flags"] = OrderedDict([
        (k, False)
        for k in 'UF_NODUMP UF_IMMUTABLE UF_APPEND UF_OPAQUE UF_NOUNLINK'
                 ' UF_COMPRESSED UF_HIDDEN SF_ARCHIVED SF_IMMUTABLE'
                 ' SF_APPEND SF_NOUNLINK SF_SNAPSHOT'.split()
    ])
    assert stat2dict(st_linux, human_names=True) == st_linux_dict

def test_freebsd():
    st_freebsd_dict = st_dict.copy()
    st_freebsd_dict["st_gen"] = 0
    st_freebsd_dict["st_birthtime"] = OrderedDict([
        ("seconds", 1535380109.4635055),
        ("iso8601", "2018-08-27T10:28:29.463506-04:00"),
    ])
    assert stat2dict(st_freebsd) == st_freebsd_dict

def test_freebsd_human_names():
    st_freebsd_dict = st_human_dict.copy()
    st_freebsd_dict["generation"] = 0
    st_freebsd_dict["creation_time"] = OrderedDict([
        ("seconds", 1535380109.4635055),
        ("iso8601", "2018-08-27T10:28:29.463506-04:00"),
    ])
    assert stat2dict(st_freebsd, human_names=True) == st_freebsd_dict

# Test stat results with both Linux and FreeBSD fields?
