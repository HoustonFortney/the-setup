# The Setup

Ansible playbook to configure a machine with my dev environment

## Run the tests

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```
uv run ansible-lint
uv run molecule test
```

## Deploy the setup

To deploy the setup on localhost:

```
uv run ansible-playbook playbook.yaml
```

