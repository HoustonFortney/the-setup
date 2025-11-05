def test_packages_are_installed(host):
    package = host.package("alacritty")
    assert package.is_installed, "Package alacritty should be installed"


def test_alacritty_config_file_exists(host):
    user = host.user()
    config_file_path = f"{user.home}/.config/alacritty/alacritty.toml"
    config_file = host.file(config_file_path)
    assert config_file.is_file, f"Alacritty config file {config_file_path} should exist"


def test_alacritty_theme_is_populated(host):
    user = host.user()
    theme_dir_path = f"{user.home}/.config/alacritty/themes"
    theme_dir = host.file(theme_dir_path)
    assert theme_dir.is_directory, f"Alacritty theme directory {theme_dir_path} should exist"
    assert theme_dir.size > 0, f"Alacritty theme directory {theme_dir_path} should not be empty"
