resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "fastappdns"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
  }

  depends_on = []
}

resource "azurerm_kubernetes_cluster_node_pool" "additional_pool" {
  name                = "fastappnp"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size             = "Standard_B2s"
  node_count          = var.node_count
  mode                = "User"
}


output "aks_kube_config" {
  value = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

