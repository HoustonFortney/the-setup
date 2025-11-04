def test_vimrc_exists(host):
    user = host.user()
    vimrc = host.file(f"{user.home}/.vimrc")
    assert vimrc.exists, "The .vimrc file should exist."
