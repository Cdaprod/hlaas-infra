# cdaLab Ansible Role

## Overview
This Ansible role is designed to configure and manage cdaLab environments.

## Requirements
- Ansible version 2.9 or higher.

## Role Variables
- `packages`: List of packages to install.

## Dependencies

## Example Playbook

```yaml
- hosts: servers
  roles:
     - { role: cdaLab }
```

## License

MIT - David Cannan 2024

This role was created in 2023 by David Cannan for Cdaprod.