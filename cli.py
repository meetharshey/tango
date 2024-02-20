import shutil
import subprocess
import click
import os
from PyInquirer import prompt

class ConfigResponse:
    def __init__(self, project_name, automation_framework, cloud_provider, aws_account_id=None, aws_default_region=None, project_dir=None):
        self.project_name = project_name
        self.automation_framework = automation_framework
        self.cloud_provider = cloud_provider
        self.aws_account_id = aws_account_id
        self.aws_default_region = aws_default_region
        self.project_dir = project_dir

class NonEmptyStringValidator(click.ParamType):
    name = 'non_empty_string'

    def convert(self, value, param, ctx):
        if not value.strip():
            self.fail('Value cannot be empty.', param, ctx)
        return value.strip()

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}  # Initialize a dictionary to store objects

@cli.command()
def version():
    click.echo("Tango module has been installed successfully.")

@cli.command()
@click.pass_context
def init(ctx):
    # Prompt user for project details
    project_name = click.prompt("Enter Project Name", type=NonEmptyStringValidator())

    # Prompt user for automation framework
    automation_framework_choices = ['Selenium', 'Playwright', 'Puppeteer']
    questions = [
        {
            'type': 'list',
            'name': 'automation_framework',
            'message': 'Select Automation Framework:',
            'choices': automation_framework_choices
        }
    ]
    answers = prompt(questions)
    automation_framework = answers['automation_framework']

    # Prompt user for cloud provider
    cloud_provider_choices = ['AWS', 'Azure']
    questions = [
        {
            'type': 'list',
            'name': 'cloud_provider',
            'message': 'Select Cloud Provider:',
            'choices': cloud_provider_choices
        }
    ]
    answers = prompt(questions)
    cloud_provider = answers['cloud_provider']

    # Store responses in a config object
    config = ConfigResponse(project_name, automation_framework, cloud_provider)

    # Store config object in the context
    ctx.obj['config'] = config

    # Create project directory structure
    create_project(config)

def create_project(config):
    # Create project directory
    project_dir = config.project_name.replace(" ", "_")
    # os.makedirs(project_dir)
    result = subprocess.run(['ls'], capture_output=True, text=True)
    print(result.stdout)
    # Copy contents of /app/aws or /app/azure into the project directory
    if config.cloud_provider == "AWS":
        source_dir = 'app/aws/'
    elif config.cloud_provider == "Azure":
        source_dir = 'app/azure'
    else:
        click.echo("Error: Unknown cloud provider.")
        return

    if os.path.exists(source_dir):
        shutil.copytree(source_dir, project_dir)
    else:
        click.echo("Error: Source directory does not exist.")
    if not (os.path.exists(project_dir)):
        click.echo("Error: Unable to create project directory")

    # Save project directory path in config
    config.project_dir = project_dir

@cli.command()
@click.pass_context
def build(ctx):
    # Docker file, install dependencies - chromium, selenium
    # Check if Docker is installed and Docker daemon is running
    try:
        subprocess.run(['docker', '--version'], check=True)
        subprocess.run(['docker', 'info'], check=True)
    except subprocess.CalledProcessError:
        click.echo("Error: Docker is not installed or Docker daemon is not running.")
        return

    # Access the config object from the context
    config = ctx.obj.get('config')

    if config is None:
        click.echo("Error: Config object not found. Please run 'init' command first.")
        return
    else:
        print(config)

    # Change directory to the project directory
    os.chdir(config.project_dir)

    # Build the Docker image
    try:
        subprocess.run(['docker', 'build', '-t', 'myapp', '.'], check=True)
    except subprocess.CalledProcessError:
        click.echo("Error: Failed to build Docker image.")
        return

    # Run the Docker container
    try:
        subprocess.run(['docker', 'run', '-i', '-v', f'{os.getcwd()}/python:/opt/ext', '-t', 'myapp'], check=True)
    except subprocess.CalledProcessError:
        click.echo("Error: Failed to run Docker container.")
        return

@cli.command()
@click.pass_context
def run(ctx):
    # Scrapper script locally in Docker container
    # Business logic
    pass

@cli.command()
@click.pass_context
def deploy(ctx):
    # Access the config object from the context
    config = ctx.obj.get('config')

    if config is None:
        click.echo("Error: Config object not found. Please run 'init' command first.")
        return
    else:
        print(config)

    # Your deployment logic using the config object goes here
    click.echo("Deploying using config:")
    click.echo(f"Project Name: {config.project_name}")
    click.echo(f"Automation Framework: {config.automation_framework}")
    click.echo(f"Cloud Provider: {config.cloud_provider}")

    if config.cloud_provider == "AWS":
        deploy_aws(ctx, config)
    elif config.cloud_provider == "Azure":
        deploy_azure(ctx, config)

def deploy_aws(ctx, config):
    # Check if AWS_ACCOUNT_ID and AWS_DEFAULT_REGION are already set
    if not config.aws_account_id:
        aws_account_id = click.prompt("Enter AWS Account ID", type=str)
        ctx.obj['config'].aws_account_id = aws_account_id
    else:
        aws_account_id = config.aws_account_id

    if not config.aws_default_region:
        aws_default_region = click.prompt("Enter Default Region", type=click.Choice(["us-east", "us-west"]))
        ctx.obj['config'].aws_default_region = aws_default_region
    else:
        aws_default_region = config.aws_default_region

    # Bootstrap "cdk bootstrap aws://your AWS ID/region"
    subprocess.run(["cdk", "bootstrap", f"aws://{aws_account_id}/{aws_default_region}"])

    # Deploy stack
    click.echo("Deploying CloudFormation stack...") 
    subprocess.run(["cdk", "deploy"])

def deploy_azure(ctx, config):
    pass

if __name__ == "__main__":
    cli()  # Passing an empty object as default context
