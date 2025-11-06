from pathlib import Path

import yaml


def load_role_defaults():
    with open("../../roles/install_i3/defaults/main.yaml", "r") as f:
        return yaml.safe_load(f)


def test_packages_are_installed(host):
    packages = load_role_defaults().get("install_i3_packages", [])
    assert packages, "Package list should not be empty"

    for package_name in packages:
        package = host.package(package_name)
        assert package.is_installed, f"Package {package_name} should be installed"


def test_i3_config_file_exists(host):
    user = host.user()
    config_file_path = f"{user.home}/.config/i3/config"
    config_file = host.file(config_file_path)
    assert config_file.is_file, f"I3 config file {config_file_path} should exist"


def test_i3blocks_config_file_exists(host):
    user = host.user()
    config_file_path = f"{user.home}/.config/i3blocks/config"
    config_file = host.file(config_file_path)
    assert config_file.is_file, f"I3blocks config file {config_file_path} should exist"


def find_scripts():
    scripts_dir = Path("../../roles/install_i3/files/scripts")
    return [p.name for p in scripts_dir.iterdir() if p.is_file()]


def test_i3_related_scripts_are_present_and_executable(host):
    scripts = find_scripts()
    assert scripts, "List of scripts to check should not be empty"

    for script in scripts:
        command = host.run(f"which {script}")
        assert command.rc == 0, f"Script {script} should be present and executable"


def test_rofi_config_is_populated(host):
    user = host.user()
    rofi_config_path = f"{user.home}/.config/rofi/config.rasi"
    rofi_config = host.file(rofi_config_path)
    assert rofi_config.is_file, f"Rofi config file {rofi_config_path} should exist"
    assert rofi_config.size > 0, f"Rofi config file {rofi_config_path} should not be empty"
