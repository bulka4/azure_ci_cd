from pathlib import Path
import os, sys

classes_path = Path(Path(__file__).parent.parent.parent / 'classes').resolve().as_posix()
sys.path.append(classes_path)

from dotenv import load_dotenv
import json

from class_connection_service import ServiceConnection

# Load environment variables from the .env file
load_dotenv()

sc = ServiceConnection(
    token = os.getenv('AZURE_DEVOPS_PAT')
    ,organization = os.getenv('DEVOPS_ORGANIZATION')
    ,project = os.getenv('DEVOPS_PROJECT')
)

sc.get_services()

print(json.dumps(sc.scices, indent = 1))