import json


def load_role_settings():
    with open("../../roles/install_claude_code/files/settings.json", "r") as f:
        return json.load(f)


def test_claude_code_is_installed(host):
    command = host.run("~/.local/bin/claude --version")
    assert command.rc == 0, "Claude Code should be installed and executable"


def test_settings_file_deployed(host):
    user = host.user()
    settings = host.file(f"{user.home}/.claude/settings.json")
    assert settings.exists, "Claude Code settings.json should be deployed"
    deployed = json.loads(settings.content_string)
    assert deployed == load_role_settings(), "Deployed settings should match the managed source"
