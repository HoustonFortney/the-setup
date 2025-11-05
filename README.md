# The Setup

An Ansible playbook for automated configuration of a complete Linux development environment. This playbook installs and configures essential development tools, utilities, and custom workflows to get you up and running quickly on a fresh system.

## 🎯 Purpose

This project automates the tedious process of setting up a development machine from scratch. Whether you're configuring a new laptop, a virtual machine, or recovering from a system reinstall, this playbook handles all the heavy lifting to get your environment configured exactly the way you like it.

## 📋 Prerequisites

- **Operating System**: Ubuntu/Debian-based Linux distribution (tested on Ubuntu 22.04 Jammy)
- **Python**: Version 3.12 or higher
- **uv**: Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Sudo Access**: Required for installing system packages

### Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🚀 Quick Start

1. Clone this repository:
   ```bash
   git clone <your-fork-url>
   cd the-setup
   ```
   (Replace `<your-fork-url>` with the actual repository URL)

2. Run the playbook to configure your system:
   ```bash
   uv run ansible-playbook playbook.yaml
   ```

3. Follow any prompts and wait for the configuration to complete.

## 🔧 What Gets Installed

This playbook configures your system with the following components:

### System Utilities
- **Command-line tools**: `unzip`, `tree`, `jq`, `traceroute`, `tmux`, `speedtest-cli`
- Essential development and debugging utilities

### Shell Configuration
- **Bash customization**: Custom `.bashrc_local` configuration with personalized settings
- **Aliases**: Pre-configured bash aliases for common commands
- Automatic sourcing of custom configuration files

### Text Editor
- **Vim**: Configured with custom settings for an enhanced editing experience

### Window Manager
- **i3**: Tiling window manager with custom configuration
- **Rofi**: Application launcher integration
- Machine-specific display configuration support
- Custom i3 scripts installed to `/usr/local/bin`

### Version Control
- **Git**: Configured with user preferences and aliases

### Containerization
- **Docker**: Docker engine and related tools for container development

### Programming Languages & Tools
- **Python**: `uv` package manager for fast, reliable Python dependency management
- **Node.js**: Latest LTS version from NodeSource repository
- **npm**: Node package manager included with Node.js

### Infrastructure Tools
- **Terraform**: Infrastructure as Code tool for cloud provisioning
- **AWS CLI**: Amazon Web Services command-line interface
- **kubectl**: Kubernetes command-line tool for cluster management
- **Helm**: Kubernetes package manager

### Custom Scripts
- **quick-run**: Persistent process manager for rapid command re-execution
- **quick-run-go**: Signal script to trigger quick-run commands
- Located in `/usr/local/bin` for system-wide access

## 🧪 Testing

This project uses [Molecule](https://molecule.readthedocs.io/) with Vagrant and VirtualBox to test the Ansible roles in an isolated environment.

### Prerequisites for Testing
- VirtualBox
- Vagrant
- Python dependencies (managed by uv)

### Run Tests

```bash
# Lint the Ansible playbook
uv run ansible-lint

# Run full integration tests (creates VM, applies playbook, runs tests)
uv run molecule test
```

The test suite:
1. Creates a fresh Ubuntu 22.04 VM using Vagrant
2. Applies all roles from the playbook
3. Verifies correct installation using testinfra
4. Tests idempotency (running twice produces same result)
5. Cleans up the test environment

## 🎨 Customization

### Modifying Installed Packages

You can customize what gets installed by editing the defaults in each role:

- **Utilities**: Edit `roles/install_utils/defaults/main.yaml`
- **Node.js version**: Edit `roles/install_nodejs/defaults/main.yaml`
- **i3 packages**: Edit `roles/install_i3/defaults/main.yaml`
- **Infrastructure tools**: Edit `roles/install_infrastructure_tools/defaults/main.yaml`

### Adding Your Own Configuration Files

Each role can include custom configuration files:

- **Bash**: Add custom bash config to `roles/configure_bash/files/`
- **Vim**: Modify vim config in `roles/configure_vim/files/`
- **i3**: Customize i3 window manager in `roles/install_i3/files/`
- **Git**: Update git config in `roles/configure_git/tasks/`

### Running Specific Roles

To run only specific roles instead of the entire playbook, you can use Ansible's `--limit` option or modify the playbook. For example, to run only specific roles, you could create a custom playbook or comment out roles you don't want to run in `playbook.yaml`.

### Targeting Remote Hosts

By default, the playbook runs on localhost. To target remote hosts:

1. Edit `hosts.yaml` to add your remote hosts. Example:
   ```yaml
   all:
     hosts:
       remote-server:
         ansible_host: 192.168.1.100
         ansible_user: your-username
   ```
2. Ensure SSH access is configured
3. Run: `uv run ansible-playbook playbook.yaml -i hosts.yaml`

## 📁 Project Structure

```
.
├── playbook.yaml              # Main playbook that orchestrates all roles
├── hosts.yaml                 # Inventory file (defaults to localhost)
├── ansible.cfg                # Ansible configuration
├── pyproject.toml             # Python dependencies
├── roles/                     # Ansible roles directory
│   ├── install_utils/         # System utilities
│   ├── configure_bash/        # Bash shell configuration
│   ├── configure_vim/         # Vim editor configuration
│   ├── install_i3/            # i3 window manager
│   ├── configure_git/         # Git configuration
│   ├── install_docker/        # Docker installation
│   ├── quick_run/             # Quick-run utility scripts
│   ├── install_python_tools/  # Python development tools
│   ├── install_nodejs/        # Node.js installation
│   └── install_infrastructure_tools/  # Cloud/infrastructure CLIs
└── molecule/                  # Testing configuration
    └── default/               # Default test scenario
```

## 🐛 Troubleshooting

### Permission Errors
If you encounter permission errors, ensure you have sudo access and the playbook will prompt for your password when needed.

### Package Installation Failures
- Check your internet connection
- Verify you're running on a supported Ubuntu/Debian version
- Review the specific error message in the Ansible output

### Docker Group Permissions
After Docker installation, you may need to log out and back in for group permissions to take effect, or run:
```bash
newgrp docker
```

### Vagrant/VirtualBox Testing Issues
If molecule tests fail:
- Ensure VirtualBox and Vagrant are properly installed
- Check that virtualization is enabled in your BIOS
- Verify you have enough disk space and memory

## 🤝 Contributing

Contributions are welcome! If you'd like to add new roles or improve existing ones:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests: `uv run molecule test`
5. Submit a pull request

## 📝 License

This project is for personal use. Feel free to fork and customize for your own needs.

## 🔗 Related Tools

- **Ansible**: [Official Documentation](https://docs.ansible.com/)
- **uv**: [Python Package Manager](https://docs.astral.sh/uv/)
- **Molecule**: [Ansible Testing Framework](https://molecule.readthedocs.io/)
- **i3**: [Tiling Window Manager](https://i3wm.org/)

