"""
In this class we have functions related to Service Connections.

We have here functions for example for listing, creating and deleting Service Connections.

Note: Every time we create a Service Connection in DevOps, it automatically creates a new Service Principal in Azure with a name of the format \<organization>-\<project>-xxx, 
where organization and project can be taken from DevOps URL: dev.azure.com/\<organization>/\<project>
"""


from class_devops import Devops
import requests as rq
import json

class ServiceConnection(Devops):
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


    def get_services(
        self
    ):
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/serviceendpoint/endpoints?api-version=7.1"
        response = rq.get(url, headers=self.headers)

        if response.status_code == 200:
            self.scices = response.json()
        else:
            print(f"Failed to get Service connections data. Status code: {response.status_code}")
            print(response.text)


    def find_service_id(
        self
        ,service_name
    ):
        if not hasattr(self, 'scices'):
            self.get_services()

        for service in self.scices['value']:
            if service['name'] == service_name:
                return service['id']
        

    def create_acr_service(
        self
        ,subscription_id
        ,subscription_name
        ,tenant_id
        ,sp_id # service principal application ID
        ,sp_password # service principal password
        ,acr_rg # resource group with ACR
        ,acr_name # ACR name without the .azurecr.io
        ,service_name
    ):
        """
        Note: Every time we create a Service Connection in DevOps, it automatically creates a new Service Principal in Azure with a name of the format 
        \<organization>-\<project>-xxx, where organization and project can be taken from DevOps URL: dev.azure.com/\<organization>/\<project>
        """

        acr_resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{acr_rg}/providers/Microsoft.ContainerRegistry/registries/{acr_name}"
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/serviceendpoint/endpoints?api-version=7.1"

        # data = {
        #     "authorization": {
        #         "parameters": {
        #             "tenantid": tenant_id,
        #             "serviceprincipalid": sp_id,
        #             "authenticationType": "spnKey",
        #             "serviceprincipalkey": sp_password
        #         },
        #         "scheme": "ServicePrincipal"
        #     },
        #     "data": {
        #         "subscriptionId": subscription_id,
        #         "subscriptionName": subscription_name,
        #         "registrytype": "ACR",
        #         "registryId": acr_resource_id
        #     },
        #     "name": service_name,
        #     "type": "dockerregistry",
        #     "url": f"https://{acr_name}.azurecr.io",
        #     "isShared": False,
        #     "isReady": True,
        #     "serviceEndpointProjectReferences": [
        #         {
        #             "projectReference": {
        #                 "id": self.project_id,
        #                 "name": self.project
        #             },
        #             "name": service_name
        #         }
        #     ]
        # }

        data = {
            "authorization": {
                "parameters": {
                    "loginServer": f"{acr_name.lower()}.azurecr.io",
                    "role": "8311e382-0749-4cb8-b61a-304f252e45ec", # acrpush
                    "scope": acr_resource_id,
                    "tenantId": tenant_id,
                    "workloadIdentityFederationIssuerType": "EntraID",
                    "serviceprincipalid": sp_id
                },
                "scheme": "ServicePrincipal"
            },
            "data": {
                "subscriptionId": subscription_id,
                "subscriptionName": subscription_name,
                "registrytype": "ACR",
                "registryId": acr_resource_id
            },
            "name": service_name,
            "type": "dockerregistry",
            "url": f"https://{acr_name}.azurecr.io",
            "isShared": False,
            "isReady": True,
            "serviceEndpointProjectReferences": [
                {
                    "projectReference": {
                        "id": self.project_id,
                        "name": self.project
                    },
                    "name": service_name
                }
            ]
        }


        # === MAKE THE REQUEST ===
        response = rq.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Created ACR Service connection successfully.")
            return response.json()
        else:
            print(f"Failed to create ACR Service connection. Status code: {response.status_code}")
            print(response.text)


    def delete_service(
        self
        ,service_name # Name of the service connection we want to delete
    ):
        service_id = self.find_service_id(service_name)
        url = f"https://dev.azure.com/{self.organization}/_apis/serviceendpoint//endpoints/{service_id}?projectIds={self.project_id}&api-version=7.1"

        response = rq.delete(url, headers=self.headers)

        if response.status_code in [200, 204]:
            print("Deleted ACR Service connection successfully.")
            return response.text
        else:
            print(f"Failed to delete ACR Service connection. Status code: {response.status_code}")
            print(response.text)