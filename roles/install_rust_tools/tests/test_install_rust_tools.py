def test_cargo_is_installed(host):
    command = host.run("~/.cargo/bin/cargo --version")
    assert command.rc == 0, "cargo should be installed and executable"
