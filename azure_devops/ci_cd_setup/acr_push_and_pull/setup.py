"""
This script is setting up resources needed for a CI/CD pipeline in Azure DevOps. It performs following actions:

1. Add service principal credentials to the DevOps Library:
They are used in the YAML file in order to pull an image from ACR. We will create a variable group with a specified name 
and create there variables SP_ID and SP_PASSWORD for service principal application ID and password.

2. Create a Service Connection in DevOps linked to the ACR.
We will use that Service Connection in order to push a Docker image to ACR. We will use the ID of that Service Connection
in the YAML file for the containerRegistry argument in the step for pushing image to ACR.

For creating that Service Connection we will use the same Service Principal which credentials we saved in a Library.

3. Generate the YAML file.
We will generate the YAML file defining our CI/CD pipeline. It will need to be added to the repo containing the Docker 
image which we want to deploy on VM.

Before running this script we need to create the .env file which will contain all the variables which are accessed in this script using the
os.getenv('variable_name') command. Those are:

    - AZURE_DEVOPS_PAT - personal access token from DevOps
    - SUB_ID - Azure subscription ID
    - TENANT_ID - ID of the tenant of the Service Principal
    - SP_ID - Service Principal app ID 
    - SP_PASSWORD - Service Principal password

Variables TENANT_ID, SP_ID and SP_PASSWORD are related to the Service Principal with scope for our ACR and acrpush role. It will be used 
for creating a Service Connection in DevOps to ACR and for pulling images from ACR.
"""

from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent.parent / 'classes').resolve().as_posix()
sys.path.append(classes_path)

from dotenv import load_dotenv
import pandas as pd

from class_library import Library
from class_connection_service import ServiceConnection
from class_yaml import Yaml
from class_logs import Logs


# ============= Load environment variables from the .env file =============

load_dotenv()

# Variables related to DevOps  

# name of the Agent pool which will be used for performing the CI/CD pipeline. That pool can be created using agent_pool_setup > setup.py script.
pool_name = os.getenv('POOL_NAME')
# Name of the variable group which we will create in DevOps Library
devops_variable_group_name = os.getenv('DEVOPS_VARIABLE_GROUP_NAME')

# personal access token from DevOps. It can be generated on the website
token = os.getenv('AZURE_DEVOPS_PAT')
# devops organization and project names can be taken from url: dev.azure.com/<organization>/<project>
organization = os.getenv('DEVOPS_ORGANIZATION')
project = os.getenv('DEVOPS_PROJECT')



# Variables related to the app we want to deploy

# path to the Dockerfile and docker compose files relative to the root folder of repository from which we will be deploying code.
# If both Dockerfile and docker-compose.yaml are in the repository root folder, then we can leave the below values.
dockerfile_path = os.getenv('DOCKERFILE_PATH')
docker_compose_path = os.getenv('DOCKER_COMPOSE_PATH')



# Variables related to Azure

# Name of our Azure subscription
subscription_name = os.getenv('AZURE_SUBSCRIPTION_NAME')
# Azure subscription ID
subscription_id = os.getenv('SUB_ID')

# Name of the resource group with our ACR
acr_rg = os.getenv('ACR_RG')
# Name of the ACR
acr_name = os.getenv('ACR_NAME')

# name of the image repository in ACR to which we will push our Docker image. It will be created if it doesn't exist
image_repository = os.getenv('IMAGE_REPOSITORY_NAME')
# The tag which will be assigned to the Docker image pushed to the ACR.
tag = os.getenv('IMAGE_TAG')

# ID of the tenant of the Service Principal 
tenant_id = os.getenv('TENANT_ID')
# Service Principal app ID and password
sp_id = os.getenv('SP_ID')
sp_password = os.getenv('SP_PASSWORD')







# ============ Adding variables to DevOps Library ============

# create a variable group in DevOps Library
lib = Library(
    token = token
    ,organization = organization
    ,project = project
)

response = lib.create_variable_group(
    variable_group_name = devops_variable_group_name
    ,variables = {
        'SP_ID': {
            "value": sp_id,
            "isSecret": True
        },
        'SP_PASSWORD': {
            "value": sp_password,
            "isSecret": True
        }
    }
)








# ============ Creating a Service Connection in DevOps ============
sc = ServiceConnection(
    token = token
    ,organization = organization
    ,project = project
)

response = sc.create_acr_service(
    subscription_id = subscription_id
    ,subscription_name = subscription_name
    ,tenant_id = tenant_id
    ,sp_id = sp_id
    ,sp_password = sp_password
    ,acr_rg = acr_rg
    ,acr_name = acr_name
    ,service_name = acr_name
)

acr_service_connection_id = response['id']









# ============ Generating the YAML file ============

# Create the YAML backbone
yaml = Yaml(
    pool_name = pool_name
    ,variable_group_name = devops_variable_group_name
)

# add stage for pushing a Docker image to ACR
yaml.add_stage_push_to_acr(
    image_repository
    ,acr_service_connection_id
    ,tag
    ,dockerfile_path
)

# add stage for pulling a Docker image from ACR to the VM
yaml.add_stage_deploy(
    acr_name
    ,image_repository
    ,tag
    ,docker_compose_path
)

# save the YAML file
yaml.save('azure-pipelines.yml')









# ============ Save logs about created resources in DevOps ============
logs = Logs()

new_logs = pd.DataFrame([
        [devops_variable_group_name, 'Variable group', 'created']
        ,[acr_name, 'Service connection', 'created']
    ]
    ,columns = ['resource_name', 'resource_type', 'action']
)

logs.add_logs(new_logs)
logs.save_logs()