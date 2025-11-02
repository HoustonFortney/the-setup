def test_git_config_spot_check(host):
    user = host.user()
    git_config_file = host.file(f"{user.home}/.gitconfig")
    assert git_config_file.exists
    assert git_config_file.contains("vim")
