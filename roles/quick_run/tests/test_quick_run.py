import pytest


@pytest.mark.parametrize("script", ["quick-run", "quick-run-go"])
def test_quick_run_scripts_are_present_and_executable(host, script):
    command = host.run(f"which {script}")
    assert command.rc == 0, f"Script {script} should be present and executable"


def test_quick_run_help_command(host):
    command = host.run("quick-run --help")
    assert command.rc == 0, "quick-run --help should execute successfully"
    assert "Usage:" in command.stdout


def test_quick_run_missing_command(host):
    command = host.run("quick-run")
    assert command.rc != 0, "quick-run with a missing command should fail"
    assert "Error:" in command.stderr


def test_quick_run_go_without_running_session(host):
    host.run("rm -f /tmp/quick-run.pipe")  # Ensure no active session
    command = host.run("quick-run-go")
    assert command.rc != 0, "quick-run-go without an active session should fail"
    assert "quick-run is not active" in command.stderr


def run_integration_test_sequence(host):
    host.run("rm -f test.txt")  # Clean up before test

    # Start a quick-run session
    start_command = host.run("nohup quick-run touch test.txt > /dev/null 2>&1 & echo $!")
    assert start_command.rc == 0, "Starting quick-run session should succeed"
    pid = start_command.stdout.strip()

    # Now run quick-run-go to execute the command
    go_command = host.run("quick-run-go")
    assert go_command.rc == 0, "quick-run-go should execute successfully"

    # Verify that the command was executed
    test_file = host.file("test.txt")
    assert test_file.exists, "test.txt should be created by quick-run"

    # Kill the quick-run session
    host.run(f"kill {pid}")

    # Pipe should be removed after session ends
    pipe = host.file("/tmp/quick-run.pipe")
    assert not pipe.exists, "quick-run pipe should be removed after session ends"


def test_quick_run_integration(host):
    run_integration_test_sequence(host)


def test_quick_run_operates_with_preexisting_pipe(host):
    host.run("mkfifo /tmp/quick-run.pipe")
    run_integration_test_sequence(host)
