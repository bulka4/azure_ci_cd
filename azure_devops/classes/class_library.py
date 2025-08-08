"""
In this class we have functions related to Library.

We have here functions for example for listing, creating and deleting Libraries.
"""


from class_devops import Devops

import requests as rq
import json

class Library(Devops):
    def __init__(
        self
        ,token # personall access token from the Azure DevOps website
        ,organization # Name of the DevOps organization. It can be taken from URL: https://dev.azure.com/<organization>/<project>
        ,project # Name of the DevOps project. It can be taken from URL: https://dev.azure.com/<organization>/<project>
    ):
        super().__init__(
            token
            ,organization
            ,project
        )

    def create_variable_group(
        self
        ,variable_group_name
        ,variables
    ):
        """
        The variables argument has the following format:
        variables = {
            "MyVariable1": {
                "value": "Value1",
                "isSecret": False  # Set to True for sensitive variables
            },
            "MyVariable2": {
                "value": "Value2",
                "isSecret": True  # Example of a secret variable
            }
        }
        """

        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/distributedtask/variablegroups?api-version=7.1-preview.1"
        data = {
            "name": variable_group_name,
            "variables": variables
        }
        response = rq.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Variable group created successfully.")
            return response.json()
        else:
            print(f"Failed to create variable group. Status code: {response.status_code}")
            print(response.text)


    def get_variable_groups(
        self
    ):
        """
        Get list of all variable groups and assing them to the self.variable_groups attribute.
        """

        if hasattr(self, 'variable_groups'):
            del self.variable_groups
        
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/distributedtask/variablegroups?api-version=7.1-preview.1"
        response = rq.get(url, headers=self.headers)

        if response.status_code == 200:
            self.variable_groups = response.json()['value']
        else:
            print(f"Failed to list variable groups. Status code: {response.status_code}")
            print(response.text)


    def get_variable_group_id(
        self
        ,variable_group_name
    ):
        """
        Get a variable group ID based on its name.
        """
        # if we don't have info about variable groups yet then get it.
        if not hasattr(self, 'variable_groups'):
            self.get_variable_groups()

        for group in self.variable_groups:
            if group['name'] == variable_group_name:
                return group['id']


    def delete_variable_group(
        self
        ,variable_group_name
    ):

        variable_group_id = self.get_variable_group_id(variable_group_name)
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/distributedtask/variablegroups/{variable_group_id}?api-version=7.1-preview.1"

        response = rq.delete(url, headers=self.headers)

        # Check the response
        if response.status_code == 204:
            print("Variable group deleted successfully.")
        else:
            print(f"Failed to delete variable group. Status code: {response.status_code}")
            print(response.text)
