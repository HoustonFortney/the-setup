import yaml


def load_role_defaults():
    with open("../../roles/install_nodejs/defaults/main.yaml", "r") as f:
        return yaml.safe_load(f)


def test_correct_node_version_is_installed(host):
    major_version = load_role_defaults().get("install_nodejs_major_version", None)
    assert major_version is not None, "Node.js major version should be specified"

    command = host.run("node --version")
    assert command.rc == 0, "Node.js should be installed"
    installed_version = command.stdout.strip().lstrip("v")
    installed_major_version = installed_version.split(".")[0]
    assert installed_major_version == str(major_version), f"Installed Node.js major version should be {major_version}"


def test_npm_is_executable(host):
    command = host.run("npm --version")
    assert command.rc == 0, "npm should be installed and executable"
