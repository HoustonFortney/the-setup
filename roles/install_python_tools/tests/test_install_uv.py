def test_uv_is_installed(host):
    command = host.run("~/.local/bin/uv --version")
    assert command.rc == 0, "uv should be installed and executable"
