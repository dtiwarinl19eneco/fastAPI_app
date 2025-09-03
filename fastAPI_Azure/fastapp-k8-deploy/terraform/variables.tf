variable "resource_group_name" {
  default = "fastapp-rg"
}

variable "location" {
  default = "westeurope"
}

variable "aks_cluster_name" {
  default = "fastapp-aks"
}

variable "acr_name" {
  default = "myacrfastapp"
}

variable "node_count" {
  default = 1
}

variable "k8s_namespace" {
  default = "default"
}

