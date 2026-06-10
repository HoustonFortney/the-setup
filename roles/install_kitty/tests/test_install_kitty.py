def test_packages_are_installed(host):
    package = host.package("kitty")
    assert package.is_installed, "Package kitty should be installed"


def test_kitty_config_file_exists(host):
    user = host.user()
    config_file_path = f"{user.home}/.config/kitty/kitty.conf"
    config_file = host.file(config_file_path)
    assert config_file.is_file, f"kitty config file {config_file_path} should exist"


def test_kitty_theme_is_populated(host):
    user = host.user()
    theme_dir_path = f"{user.home}/.config/kitty/themes"
    theme_dir = host.file(theme_dir_path)
    assert theme_dir.is_directory, f"kitty theme directory {theme_dir_path} should exist"
    assert theme_dir.size > 0, f"kitty theme directory {theme_dir_path} should not be empty"
