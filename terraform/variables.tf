variable "resource_group_location" {
  type        = string
  description = "Location of the resource group."
  default = "westeurope"
}

variable "resource_group_name" {
  type        = string
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
  default = "data_engineering_apps"
}

variable acr_name {
  type = string
  description = "Name of the container registry."
  default = "dataEngineeringApps"
}

variable service_principal_display_name {
  type = string
  description = "Name of the Service Principal."
  default = "data_engineering_apps_acr"
}

variable service_principal_role {
  type = string
  description = <<EOF
    Role assigned to the created Service Principal. The 'acrpush' role will allow for both pushing and pulling images to ACR.
    The 'pull' role allow only for pulling.
  EOF
  default = "acrpush"
}

variable "vm_username" {
  type        = string
  description = "The username for the local account that will be created on the new VM."
  default = "azureadmin"
}

variable "ssh_folder" {
  type        = string
  description = "Path to the folder where ssh key should be saved. On Windows the default one is C:/Users/<username>/.ssh/id_rsa. It is the easiest to use."
}


# Below variables starting with 'azure_pipelines_' are needed in order to install an Azure Pipelines Self Hosted Agent on the created VM.

variable azure_pipelines_url {
  type = string
  description = "URL of the Azure devOps organization which we will be using. It has the following format: https://dev.azure.com/<organization_name>"
}

variable agent_download_url {
  type = string
  description = <<EOF
    URL for downloading Self Hosted Agent. More information about how to get this URL is here: 
    https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/linux-agent
    In the 'Download and configure the agent' section.
  EOF
}

variable azure_pipelines_token {
  type        = string
  description = "Personall access token to the Azure DevOps. It can be obtained from the DevOps website."
  sensitive   = true
}

variable azure_pipelines_pool_name {
  type = string
  description = "Name of the Agent pool to which we will add created Agent."
}

variable azure_pipelines_agent_name {
  type = string
  description = "Name of the Agent that we will create."
  default = "myAgent"
}