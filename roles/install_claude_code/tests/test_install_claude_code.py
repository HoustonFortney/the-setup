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


def test_status_line_script_deployed(host):
    user = host.user()
    script = host.file(f"{user.home}/.claude/statusline.py")
    assert script.exists, "Status line script should be deployed"
    assert script.mode & 0o100, "Status line script should be executable"


def test_notification_hook_deployed(host):
    user = host.user()
    script = host.file(f"{user.home}/.claude/notify-tmux.sh")
    assert script.exists, "Notification hook script should be deployed"
    assert script.mode & 0o100, "Notification hook script should be executable"


def test_global_instructions_deployed(host):
    user = host.user()
    instructions = host.file(f"{user.home}/.claude/CLAUDE.md")
    assert instructions.exists, "Global CLAUDE.md should be deployed"
