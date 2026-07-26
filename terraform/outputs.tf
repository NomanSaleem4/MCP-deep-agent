output "acr_login_server" {
  description = "ACR Login Server Domain"
  value       = azurerm_container_registry.acr.login_server
}

output "fastapi_public_url" {
  description = "Direct Public URL for FastAPI Application"
  value       = "https://${azurerm_container_app.app.ingress[0].fqdn}"
}