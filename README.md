# Home Lab as a Service - Infrastructure Repository
This is the infrastructure repository for Home Lab as a Service.

## Repos:
- [hlaas-platform](https://github.com/cdaprod/hlaas-platform)
- [hlaas-infra](https://github.com/cdaprod/hlaas-infra) (self)
- [hlaas-ci-cd](https://github.com/cdaprod/hlaas-ci-cd)
- [hlaas-docs](https://github.com/cdaprod/hlaas-docs)

```
hlaas-infra/
├── ansible/
│   ├── roles/
│   │   ├── webserver/
│   │   ├── database/
│   │   └── monitoring/
│   ├── inventory/
│   │   └── dynamic.py
│   └── playbooks/
│       └── site.yml
├── terraform/
│   ├── modules/
│   │   ├── network/
│   │   ├── compute/
│   │   └── storage/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── main.tf
├── docker/
│   └── Dockerfile
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── .github/
│   ├── workflows/
│   │   ├── terraform.yml
│   │   ├── ansible-lint.yml
│   │   └── docker-build.yml
├── .gitignore
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

# Main Python Script Docs

## Deployment and Configuration Script Documentation

This documentation outlines the functions defined in the script for deploying and configuring infrastructure using Terraform and Ansible.

## CommandRunner Class

### `__init__` Method

```python
def __init__(self, logger=None):
    self.logger = logger or logging.getLogger(__name__)
```
Initializes the CommandRunner instance with an optional logger.

### `run_command` Method

```python
def run_command(self, command, **kwargs):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, **kwargs)
        self.logger.info(output.decode())
    except subprocess.CalledProcessError as e:
        self.logger.error(f"Command failed: {command}\nError: {e.output.decode()}")
        sys.exit(1)
```
Executes a shell command with additional keyword arguments and logs the output or error.

## InfrastructureManager Class

### `__init__` Method

```python
def __init__(self, runner):
    self.runner = runner
```
Initializes the InfrastructureManager with a CommandRunner instance.

### `deploy_infrastructure` Method

```python
def deploy_infrastructure(self):
    self.runner.run_command("terraform init")
    self.runner.run_command("terraform apply -auto-approve")
```
Deploys infrastructure using Terraform commands.

### `configure_infrastructure` Method

```python
def configure_infrastructure(self):
    self.runner.run_command("ansible-playbook -i ansible/inventory/dynamic.py ansible/playbooks/site.yml")
```
Configures infrastructure using Ansible playbooks.

## Main Function

```python
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    runner = CommandRunner(logging)
    manager = InfrastructureManager(runner)
    
    logging.info("Starting Home Lab as a Service deployment...")
    manager.deploy_infrastructure()
    manager.configure_infrastructure()
    logging.info("Deployment and configuration completed successfully.")
```
The entry point of the script, setting up logging, initializing class instances, and orchestrating the deployment and configuration processes.
