# Descriptions of all the variables in this file can be found in the variables.tf file.



# ============= Variables for which we can leave the default values =============

resource_group_location = "westeurope" 
resource_group_name = "data_engineering_apps" 

service_principal_display_name = "data_engineering_apps_acr" 
vm_username = "azureadmin" 
azure_pipelines_agent_name = "myAgent"



# ============= Variables for which we shouldn't be changing values. If we want to change them, then we need to change other parts of the code. =============

acr_name = "dataEngineeringApps"
azure_pipelines_pool_name = "data_engineering_apps"
service_principal_role = "acrpush"



# ============= Variables for which we need to provide correct values. =============

ssh_folder = "C:/Users/username/.ssh/id_rsa" 

azure_pipelines_url = "https://dev.azure.com/your_account_name" 
agent_download_url = "https://download.agent.dev.azure.com/agent/4.259.0/vsts-agent-linux-x64-4.259.0.tar.gz" # example link. It might be outdated
azure_pipelines_token = "your_token" 