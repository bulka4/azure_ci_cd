output "client_id" {
  description = "The Azure AD service principal's application (client) ID."
  value       = azuread_application.this.client_id
}

output "client_password" {
  description = "The Azure AD service principal's client secret value."
  value       = azuread_service_principal_password.this.value
  sensitive   = true
}

output "tenant_id" {
  value = data.azurerm_client_config.current.tenant_id
  description = <<EOF
    Tenant ID of the currently authenticated account (used by Terraform) and also of the created Service Principal (since we are creating that Service Principal
    in the same Tenant).
  EOF
}