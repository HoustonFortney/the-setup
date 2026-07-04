import pytest


@pytest.mark.parametrize("command", ["aws", "terraform", "kubectl", "helm"])
def test_infrastructure_tools_are_executable(host, command):
    command = host.run(f"which {command}")
    assert command.rc == 0, f"Script {command} should be present and executable"


@pytest.mark.parametrize(("alias_name", "target"), [("tf", "terraform"), ("kc", "kubectl")])
def test_infrastructure_aliases_are_loaded(host, alias_name, target):
    result = host.run(f"bash -i -c 'alias {alias_name}'")
    assert result.rc == 0, f"Alias {alias_name} should be defined"
    assert target in result.stdout
