output "production_webapp_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "production_webhook_url" {
  value = "https://${azurerm_linux_web_app.main.site_credential[0].name}:${azurerm_linux_web_app.main.site_credential[0].password}@${azurerm_linux_web_app.main.name}.scm.azurewebsites.net/docker/hook"
  sensitive = true
}

output "MONGODB_CONN" {
   value = "mongodb://${azurerm_cosmosdb_account.main.primary_mongodb_connection_string}};"
   sensitive   = true
}

output "test_webapp_url" {
  value = "https://${azurerm_linux_web_app.test.default_hostname}"
}

output "test_webhook_url" {
  value = "https://${azurerm_linux_web_app.test.site_credential[0].name}:${azurerm_linux_web_app.test.site_credential[0].password}@${azurerm_linux_web_app.test.name}.scm.azurewebsites.net/docker/hook"
  sensitive = true
}

output "TEST_MONGODB_CONN" {
   value = "mongodb://${azurerm_cosmosdb_account.test.primary_mongodb_connection_string};"
   sensitive   = true
}