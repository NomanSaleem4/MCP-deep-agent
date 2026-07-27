variable "project_name" {
  type        = string
  description = "Project identifier prefix"
  default     = "aiagent"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "prod"
}

variable "location" {
  type        = string
  description = "Target Azure Region"
  default     = "uaenorth"
}

variable "storage_account_suffix" {
  type        = string
  description = "Unique suffix from your bootstrap storage account"
  default     = "sttfstatef08f6b6c"
}

variable "app_image" {
  type        = string
  description = "Initial Docker image tag"
  default     = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}

variable "azure_ai_endpoint" {
  type        = string
  description = "Azure AI Endpoint URL"
  default     = ""
}

variable "azure_ai_api_key" {
  type        = string
  description = "Azure AI API Key"
  sensitive   = true
  default     = ""
}

variable "azure_ai_model" {
  type        = string
  description = "Azure AI Deployment Model Name"
  default     = ""
}