"""
This is the main class for working with DevOps. It is a parent to every other class.

It is mainly used for authentication. We create here self.headers attribute which can be used as headers when making a Rest API call,
so we don't need to create it multiple times.

We have here also general functions related to entire DevOps, not to a specific funcitionality of DevOps, like for example Agent Pool,
Service Connection, or Library.
"""

import requests as rq
import base64

class Devops:
    def __init__(
        self
        ,token # personall access token from the Azure DevOps website
        ,organization # Name of the DevOps organization. It can be taken from URL: https://dev.azure.com/<organization>/<project>
        ,project # Name of the DevOps project. It can be taken from URL: https://dev.azure.com/<organization>/<project>
    ):

        self.organization = organization
        self.project = project
        
        # === AUTH HEADER ===
        authorization = base64.b64encode(f":{token}".encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {authorization}"
        }

        # get ID of the current project
        self.get_project_id()


    def get_project_id(
        self
    ):
        response = rq.get(
            url = f'https://dev.azure.com/{self.organization}/_apis/projects?api-version=5.0-preview.3'
            ,headers = self.headers
        )

        if response.status_code == 200:
            for project in response.json()['value']:
                if project['name'] == self.project:
                    self.project_id = project['id']
        else:
            print('Failed to get project ID')
            print(response.text)