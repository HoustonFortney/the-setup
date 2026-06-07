def test_claude_code_is_installed(host):
    command = host.run("~/.local/bin/claude --version")
    assert command.rc == 0, "Claude Code should be installed and executable"
