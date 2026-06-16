import pytest
import yaml


def load_role_defaults():
    with open("../../roles/install_utils/defaults/main.yaml", "r") as f:
        return yaml.safe_load(f)


def test_packages_are_installed(host):
    packages = load_role_defaults().get("install_utils_packages", [])
    assert packages, "Package list should not be empty"

    for package_name in packages:
        package = host.package(package_name)
        assert package.is_installed, f"Package {package_name} should be installed"


@pytest.mark.parametrize(("alias_name", "target"), [("fd", "fdfind"), ("cat", "batcat")])
def test_utility_aliases_are_loaded(host, alias_name, target):
    result = host.run(f"bash -i -c 'alias {alias_name}'")
    assert result.rc == 0, f"Alias {alias_name} should be defined"
    assert target in result.stdout


def test_clipboard_helpers_file_deployed(host):
    user = host.user()
    clipboard = host.file(f"{user.home}/.bash_clipboard")
    assert clipboard.exists, "Clipboard helpers file should be deployed"


@pytest.mark.parametrize("function_name", ["yank", "yank-wd", "yank-cmd", "put"])
def test_clipboard_functions_are_loaded(host, function_name):
    result = host.run(f"bash -i -c 'type -t {function_name}'")
    assert result.rc == 0, f"Clipboard function {function_name} should be defined"
    assert result.stdout.strip() == "function"
