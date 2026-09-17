import json
from pathlib import Path

import pytest

CONFIG_FILE_MODE = 0o644


def test_codex_is_installed(host):
    result = host.run("~/.local/bin/codex --version")
    assert result.rc == 0
    assert "codex-cli" in result.stdout


@pytest.mark.parametrize("name", ["config.toml", "AGENTS.md", "rules/the-setup.rules"])
def test_codex_configuration_deployed(host, name):
    source = Path(__file__).resolve().parents[1] / "files" / name
    deployed = host.file(f"{host.user().home}/.codex/{name}")
    assert deployed.exists
    assert deployed.mode == CONFIG_FILE_MODE
    assert deployed.content_string == source.read_text()


def test_codex_accepts_configuration(host):
    result = host.run("~/.local/bin/codex doctor --json")
    checks = json.loads(result.stdout)["checks"]
    # Login and runtime checks can fail in fresh containers; config must pass.
    for name, check in checks.items():
        if name.startswith("config."):
            assert check["status"] == "ok", check
    assert checks["config.load"]["status"] == "ok"


@pytest.mark.parametrize(
    ("command", "decision"),
    [
        ("git status --short", "allow"),
        ("git diff --stat", "allow"),
        ("rg --files", "allow"),
        ("ruff check .", "allow"),
        ("git commit -m example", "prompt"),
        ("git push origin main", "prompt"),
    ],
)
def test_codex_command_rules(host, command, decision):
    # The policy checker evaluates arguments without executing the command.
    result = host.run(
        "~/.local/bin/codex execpolicy check --rules ~/.codex/rules/the-setup.rules -- " + command,
    )
    assert result.rc == 0, result.stderr
    assert json.loads(result.stdout)["decision"] == decision
