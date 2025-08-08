"""
In this class we have functions related to Agent Pools.

We have here functions for example for listing, creating and deleting Agent Pools.
"""


from class_devops import Devops

import requests as rq
import json

class AgentPool(Devops):
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


    def get_agent_pools(
        self
    ):
        url = f'https://dev.azure.com/{self.organization}/_apis/distributedtask/pools?api-version=6.0'
        response = rq.get(url, headers=self.headers)

        self.pools = response.json()['value']

        if response.status_code == 200:
            self.pools = response.json()['value']
        else:
            print(f"Failed to get Agent pools data. Status code: {response.status_code}")
            print(response.text)


    def find_agent_pool_id(
        self
        ,name
    ):
        if not hasattr(self, 'pools'):
            self.get_agent_pools()

        for pool in self.pools:
            if pool['name'] == name:
                return pool['id']


    def create_agent_pool(
        self
        ,name
    ):
        url = f'https://dev.azure.com/{self.organization}/_apis/distributedtask/pools?api-version=6.0'
        data = {
            "name": name,  # Replace with your desired pool name
            "autoProvision": True,
            "autoUpdate": True,
            "isHosted": False,
            "poolType": "automation"
        }

        response = rq.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Agent pool created successfully.")
            return response.json()
        else:
            print(f"Failed to create agent pool. Status Code: {response.status_code}")
            print("Response:", response.text)


    def delete_agent_pool(
        self
        ,name
    ):
        pool_id = self.find_agent_pool_id(name)
        url = f'https://dev.azure.com/{self.organization}/_apis/distributedtask/pools/{pool_id}?api-version=6.0'

        response = rq.delete(url, headers = self.headers)

        if response.status_code == 200:
            print(f"Agent pool {name} deleted successfully.")
        elif response.status_code == 204:
            print(f"Agent pool {name} deleted successfully (no content).")
        else:
            print(f"Failed to delete agent pool. Status code: {response.status_code}")
            print(response.text)
