import pytest


def test_neovim_is_installed(host):
    result = host.run("nvim --version")
    assert result.rc == 0, "Neovim should be installed and executable"


def test_config_dir_is_populated(host):
    user = host.user()
    config_dir_path = f"{user.home}/.config/nvim"
    config_dir = host.file(config_dir_path)
    assert config_dir.is_directory, f"Neovim config directory {config_dir_path} should exist"
    assert config_dir.size > 0, f"Neovim config directory {config_dir_path} should not be empty"


@pytest.mark.parametrize(
    ("alias_name", "target"),
    [("vim", "nvim"), ("vi", "nvim"), ("svi", "sudo nvim")],
)
def test_neovim_aliases_are_loaded(host, alias_name, target):
    result = host.run(f"bash -i -c 'alias {alias_name}'")
    assert result.rc == 0, f"Alias {alias_name} should be defined"
    assert target in result.stdout


def test_tvi_function_is_loaded(host):
    result = host.run("bash -i -c 'type -t tvi'")
    assert result.rc == 0, "tvi function should be defined"
    assert result.stdout.strip() == "function"
