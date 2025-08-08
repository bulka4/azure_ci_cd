"""
This is a script for deleting resources in Azure DevOps.
"""

from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent.parent / 'classes')
sys.path.append(classes_path.resolve().as_posix())

from class_library import Library
from class_connection_service import ServiceConnection
from class_logs import Logs

from dotenv import load_dotenv
import pandas as pd


# Load environment variables from the .env file
load_dotenv()

devops_variable_group_name = os.getenv('DEVOPS_VARIABLE_GROUP_NAME') # Name of the Variable group which we will delete from DevOps Library
service_name = os.getenv('ACR_NAME') # Name of the Service connection which we will delete

token = os.getenv('AZURE_DEVOPS_PAT') # personal access token from DevOps

# devops organization and project names can be taken from url: dev.azure.com/{organization}/{project}
organization = os.getenv('DEVOPS_ORGANIZATION')
project = os.getenv('DEVOPS_PROJECT')



# === Deleting the Variable group ====
lib = Library(
    token = token
    ,organization = organization
    ,project = project
)

lib.delete_variable_group(devops_variable_group_name)



# === Deleting the Service connection ===
sc = ServiceConnection(
    token = token
    ,organization = organization
    ,project = project
)

sc.delete_service(service_name)


# === Save logs about deleted resources ===
logs = Logs()

new_logs = pd.DataFrame([
        [devops_variable_group_name, 'Variable group', 'deleted']
        ,[service_name, 'Service connection', 'deleted']
    ]
    ,columns = ['resource_name', 'resource_type', 'action']
)

logs.add_logs(new_logs)
logs.save_logs()