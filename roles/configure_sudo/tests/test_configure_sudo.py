EXPECTED_MODE = 0o440


def test_sudoers_file_exists(host):
    f = host.file("/etc/sudoers.d/shutdown-nopasswd")
    assert f.exists
    assert f.mode == EXPECTED_MODE
