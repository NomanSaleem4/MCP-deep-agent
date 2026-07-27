terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }

  backend "azurerm" {
    use_azuread_auth = true
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

# 1. Primary Resource Group in UAE North
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# 2. Azure Container Registry (Basic SKU ~$5/mo)
resource "azurerm_container_registry" "acr" {
  name                = "acr${var.storage_account_suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

# 3. Managed Identity for ACA to pull images without passwords
resource "azurerm_user_assigned_identity" "identity" {
  name                = "id-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# 4. Role Assignment for ACR Pull
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.identity.principal_id
}

# 5. Log Analytics (Retains logs under 5 GB/mo free tier)
resource "azurerm_log_analytics_workspace" "logs" {
  name                = "log-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# 6. Container App Environment
resource "azurerm_container_app_environment" "env" {
  name                       = "cae-${var.project_name}-${var.environment}"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
}

# 7. Direct FastAPI Container App (Sufficient RAM for deepagents)
resource "azurerm_container_app" "app" {
  name                         = "ca-${var.project_name}-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.identity.id]
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
    identity = azurerm_user_assigned_identity.identity.id
  }

  # -------------------------------------------------------------
  # 1. REGISTER ENCRYPTED SECRET IN ACA
  # -------------------------------------------------------------
  secret {
    name  = "azure-ai-api-key"
    value = var.azure_ai_api_key
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 3

    container {
      name   = "fastapi-agent"
      image  = var.app_image
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      # ---------------------------------------------------------
      # 2. INJECT AZURE AI ENV VARS
      # ---------------------------------------------------------
      env {
        name  = "AZURE_AI_ENDPOINT"
        value = var.azure_ai_endpoint
      }

      env {
        name        = "AZURE_AI_API_KEY"
        secret_name = "azure-ai-api-key"
      }

      env {
        name  = "AZURE_AI_MODEL"
        value = var.azure_ai_model
      }
    }
  }

  depends_on = [azurerm_role_assignment.acr_pull]
}