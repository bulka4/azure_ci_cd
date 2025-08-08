variable "ssh_folder" {
    type = string
    description = "Path to a folder where the private SSH key will be saved needed to connect to the VM through SSH."
    default = "C:/Users/mbulka/.ssh/id_rsa"
}

variable "resource_group_location" {
    type = string
    description = "Resource group location. It is created by the resource_group module."
}

variable "resource_group_id" {
    type = string
    description = "ID of the resource group. It is created by the resource_group module."
}