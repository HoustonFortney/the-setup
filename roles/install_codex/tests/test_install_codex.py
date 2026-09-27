import json

import pytest


def test_bubblewrap_is_installed(host):
    assert host.package("bubblewrap").is_installed
    assert host.run("bwrap --version").rc == 0


def test_ubuntu_sandbox_apparmor_profile(host):
    if host.system_info.distribution != "ubuntu" or host.system_info.release != "24.04":
        pytest.skip("The AppArmor setup is specific to Ubuntu 24.04")
    for package in ("apparmor", "apparmor-profiles", "apparmor-utils"):
        assert host.package(package).is_installed
    assert host.file("/etc/apparmor.d/bwrap-userns-restrict").exists
    # Compile the distribution policy without loading it into the host kernel.
    result = host.run(
        "apparmor_parser --skip-kernel-load --skip-cache --base /etc/apparmor.d /etc/apparmor.d/bwrap-userns-restrict",
    )
    assert result.rc == 0, result.stderr


def test_codex_is_installed(host):
    result = host.run("~/.local/bin/codex --version")
    assert result.rc == 0
    assert "codex-cli" in result.stdout


def test_codex_system_config_deployed(host):
    assert host.file("/etc/codex/config.toml").exists


def test_codex_instructions_deployed(host):
    assert host.file(f"{host.user().home}/.codex/AGENTS.md").exists


def test_codex_rules_deployed(host):
    assert host.file(f"{host.user().home}/.codex/rules/the-setup.rules").exists


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
