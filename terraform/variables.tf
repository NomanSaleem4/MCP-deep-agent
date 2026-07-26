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