output "public_ip_address" {
  value = module.linux_vm.public_ip_address
}

output sp_id {
  value = module.service_principal.client_id
  description = "Service Principal app ID"
}

output sp_password {
  value = module.service_principal.client_password
  sensitive = true
  description = "Service Principal password"
}

output sp_tenant_id {
  value = module.service_principal.tenant_id
  description = "Tenant ID of the created Service Principal."
}