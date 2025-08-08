module "resource_group" {
  source    = "./modules/resource_group"
  name      = var.resource_group_name
  location  = var.resource_group_location
}

module "acr" {
  source                  = "./modules/acr"
  acr_name                = var.acr_name
  resource_group_name     = module.resource_group.name
  resource_group_location = module.resource_group.location
}

module "service_principal" {
  source                          = "./modules/service_principal"
  service_principal_display_name  = var.service_principal_display_name
  scope                           = module.acr.id
  role                            = var.service_principal_role
}

module "networks" {
  source                  = "./modules/networks"
  resource_group_name     = module.resource_group.name
  resource_group_location = module.resource_group.location
}

module "ssh"{
  source                  = "./modules/ssh"
  resource_group_id       = module.resource_group.id
  resource_group_location = module.resource_group.location
  ssh_folder              = var.ssh_folder
}

module "storage_account" {
  source                    = "./modules/storage_account"
  resource_group_name       = module.resource_group.name
  resource_group_location   = module.resource_group.location
}

module "linux_vm" {
  source = "./modules/linux_vm"
  
  resource_group_name     = module.resource_group.name
  resource_group_location = module.resource_group.location

  subnet_id             = module.networks.subnet_id
  nsg_id                = module.networks.nsg_id

  username    = var.vm_username
  public_key  = module.ssh.public_key

  storage_account_uri = module.storage_account.primary_blob_endpoint
}

# Render the bash script template which will be executed on the VM.
locals {
  rendered_script = templatefile("install_tools.sh.tftpl", {
    username            = var.vm_username
    url                 = var.azure_pipelines_url
    agent_download_url  = var.agent_download_url
    token               = var.azure_pipelines_token
    pool_name           = var.azure_pipelines_pool_name
    agent_name          = var.azure_pipelines_agent_name
  })
}

# execute a bash script on the VM after creating it. It will install Docker and Azure Pipelines Self Hosted Agent.
resource "azurerm_virtual_machine_extension" "my_terraform_vm_extension" {
  name                 = "hostname"
  virtual_machine_id   = module.linux_vm.id
  publisher            = "Microsoft.Azure.Extensions"
  type                 = "CustomScript"
  type_handler_version = "2.0"

  protected_settings = jsonencode({
    script = base64encode(local.rendered_script)
  })
}