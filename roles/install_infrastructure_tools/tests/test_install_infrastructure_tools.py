import pytest


@pytest.mark.parametrize("command", ["aws", "terraform", "kubectl", "helm"])
def test_infrastructure_tools_are_executable(host, command):
    command = host.run(f"which {command}")
    assert command.rc == 0, f"Script {command} should be present and executable"
