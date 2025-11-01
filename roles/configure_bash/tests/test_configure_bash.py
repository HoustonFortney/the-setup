def test_bashrc_local_file_created(host):
    user = host.user()
    bashrc_local = host.file(f"{user.home}/.bashrc_local")
    assert bashrc_local.exists


def test_bashrc_local_is_sourced(host):
    command = host.run("bash -i -c 'echo $BASHRC_LOCAL_SOURCED'")
    assert command.rc == 0
    assert command.stdout.strip() == "true"


def test_bash_aliases_file_created(host):
    user = host.user()
    bash_aliases = host.file(f"{user.home}/.bash_aliases")
    assert bash_aliases.exists


def test_bash_aliases_are_loaded(host):
    command = host.run("bash -i -c 'alias ..'")
    assert command.rc == 0, "Alias '..' not found"
