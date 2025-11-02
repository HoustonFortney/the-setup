def test_docker_installation(host):
    result = host.run("sg docker -c 'docker run --rm hello-world'")
    assert result.rc == 0, "Docker is not installed or not functioning properly"
