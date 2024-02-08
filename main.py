from fastapi import FastAPI, HTTPException
from subprocess import check_output, CalledProcessError, STDOUT
import logging
import sys

app = FastAPI()

class CommandRunner:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def run_command(self, command, **kwargs):
        """
        Execute a shell command with additional kwargs for subprocess options.
        """
        try:
            output = check_output(command, shell=True, stderr=STDOUT, **kwargs)
            self.logger.info(output.decode())
            return output.decode()
        except CalledProcessError as e:
            self.logger.error(f"Command failed: {command}\nError: {e.output.decode()}")
            raise HTTPException(status_code=500, detail=e.output.decode())

class InfrastructureManager:
    def __init__(self, runner):
        self.runner = runner

    def deploy_infrastructure(self):
        init_output = self.runner.run_command("terraform init")
        apply_output = self.runner.run_command("terraform apply -auto-approve")
        return init_output + "\n" + apply_output

    def configure_infrastructure(self):
        config_output = self.runner.run_command("ansible-playbook -i ansible/inventory/dynamic.py ansible/playbooks/site.yml")
        return config_output

@app.post("/deploy/")
def deploy_infrastructure():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    runner = CommandRunner(logging)
    manager = InfrastructureManager(runner)
    logging.info("Starting Home Lab as a Service deployment...")
    deploy_output = manager.deploy_infrastructure()
    logging.info("Deployment completed successfully.")
    return {"detail": deploy_output}

@app.post("/configure/")
def configure_infrastructure():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    runner = CommandRunner(logging)
    manager = InfrastructureManager(runner)
    logging.info("Starting configuration...")
    config_output = manager.configure_infrastructure()
    logging.info("Configuration completed successfully.")
    return {"detail": config_output}