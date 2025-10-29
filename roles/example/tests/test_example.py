def test_hello_file_exists(host):
    f = host.file("/tmp/hello.txt")
    assert f.exists
    assert f.is_file
