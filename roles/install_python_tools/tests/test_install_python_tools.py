def test_uv_is_installed(host):
    result = host.run("~/.local/bin/uv --version")
    assert result.rc == 0, "uv should be installed and executable"


def test_venv_activation_alias_is_loaded(host):
    result = host.run("bash -i -c 'alias av'")
    assert result.rc == 0, "av alias should be defined"
    assert "source .venv/bin/activate" in result.stdout
