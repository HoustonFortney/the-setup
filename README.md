# The Setup

An Ansible playbook for configuration of my development environment.

## 🎯 Purpose

This playbook installs and configures everything required to get from a fresh ubuntu install to a productive development environment with my preferred tools and settings.

## 📋 Prerequisites

- **Operating System**: Ubuntu/Debian-based Linux distribution (tested on Ubuntu 26.04 Resolute)
- **Python**: Version 3.12 or higher
- **uv**: Python package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## 🚀 Quick Start

As this repository is specific to my personal configuration, you likely want to fork it first and modify it to suit your own preferences.

1. Clone this repository:
   ```bash
   git clone <your-fork-url>
   cd the-setup
   ```
   (Replace `<your-fork-url>` with the actual repository URL)

2. Run the playbook to configure your system:
   ```bash
   uv run ansible-playbook playbook.yaml --ask-become-pass
   ```

## 🔧 What Gets Installed

This playbook installs/configures:

- [Neovim](https://neovim.io/)
- Basic operating tools: [i3](https://i3wm.org/), [rofi](https://github.com/davatorium/rofi), [Alacritty](https://github.com/alacritty/alacritty)
- Nerd Fonts
- Bash shell customization
- Development tools: [Docker](https://www.docker.com/), [Node.js](https://nodejs.org), [uv](https://github.com/astral-sh/uv), [Rust](https://www.rust-lang.org/)
- [Claude Code](https://www.claude.com/product/claude-code)
- Infrastructure tools: [Terraform](https://www.terraform.io/), [Kubernetes kubectl](https://kubernetes.io/docs/tasks/tools/), [Helm](https://helm.sh/), [aws-cli](https://aws.amazon.com/cli/)
- General utilities: `jq`, `tmux`, `traceroute`, `speedtest-cli`, etc.
- Scripts for customized workflows

## 🧪 Testing

This project uses [Molecule](https://molecule.readthedocs.io/) with the Docker driver to test the Ansible roles in isolated Ubuntu containers (`ubuntu:24.04` and `ubuntu:26.04`).

### Prerequisites for Testing
- Docker
- Python dependencies (managed by uv)

### Run Tests

```bash
# Lint the Ansible playbook
uv run ansible-lint

# Lint the python tests
uv run ruff format
uv run ruff check

# Run full integration tests (creates container, applies playbook, runs tests)
uv run molecule test
```

## 🤝 Contributing

Contributions are welcome!
This repository is by design opinionated towards my personal preferences, so please fork and adapt it to your own needs.
PRs for bugfixes, version updates, or generic improvements will be considered.

## 🔗 References

- **Ansible**: [Official Documentation](https://docs.ansible.com/)
- **uv**: [Python Package Manager](https://docs.astral.sh/uv/)
- **Molecule**: [Ansible Testing Framework](https://molecule.readthedocs.io/)
