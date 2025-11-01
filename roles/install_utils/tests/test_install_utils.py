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
