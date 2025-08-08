"""
This script is deleting a given Agent pool.
"""

from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent.parent / 'classes')
sys.path.append(classes_path.resolve().as_posix())

from class_agent_pool import AgentPool
from class_logs import Logs

from dotenv import load_dotenv
import pandas as pd


# =========== Load environment variables from the .env file ===========

load_dotenv()

# Name of the Agent Pool which we will create
token = os.getenv('AZURE_DEVOPS_PAT')
pool_name = os.getenv('POOL_NAME')
organization = os.getenv('ORGANIZATION')
project = os.getenv('PROJECT')





# =========== Delete Agent Pool ===========

pool = AgentPool(
    token = token
    ,organization = organization
    ,project = project
)

pool.delete_agent_pool(pool_name)




# # =========== Save logs about deleted agent ===========
logs = Logs()
new_logs = pd.DataFrame(
    [[pool_name, 'deleted']]
    ,columns = ['pool_name', 'action']
)
logs.add_logs(new_logs)
logs.save_logs()