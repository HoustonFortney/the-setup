def test_git_config_spot_check(host):
    user = host.user()
    git_config_file = host.file(f"{user.home}/.gitconfig")
    assert git_config_file.exists
    assert git_config_file.contains("vim")


def test_lazygit_is_installed(host):
    result = host.run("lazygit --version")
    assert result.rc == 0, "lazygit should be installed and executable"


def test_lazygit_config_uses_delta(host):
    user = host.user()
    config = host.file(f"{user.home}/.config/lazygit/config.yml")
    assert config.exists
    assert config.contains("delta")
