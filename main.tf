terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "= 3.97.1"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name     = "Cohort28_LeeVar_ProjectExercise"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "Cohort28_LeeVar_ProjectExercise"
    storage_account_name = "beagleblob"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "production-effybeagle"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = false
  lifecycle { prevent_destroy = true }

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "DisableRateLimitingResponses"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "UK West"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todo_app"
  depends_on = [azurerm_cosmosdb_account.main]
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_mongo_collection" "main" {
  name                = "todolist"
  depends_on = [azurerm_cosmosdb_mongo_database.main]
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_mongo_database.main.name
  default_ttl_seconds = "777"
    index {
    keys   = ["_id"]
    unique = true
  }
  lifecycle {
    ignore_changes = [index]
  }
}

data "azurerm_cosmosdb_account" "main" {
  name = "production-effybeagle"
  depends_on = [azurerm_cosmosdb_account.main]
  resource_group_name = data.azurerm_resource_group.main.name
}


# Create App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "production-smellybeagle-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# Create New Web App
resource "azurerm_linux_web_app" "main" {
  name                = "production-smellybeagle-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image     = "lvarnham/smellybeagle"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_ENABLE_CI" = "true"
    "DOCKER_REGISTRY_SERVER_URL" = "https://docker.io"
    "WEBSITES_PORT" = "8000"
    "FLASK_APP" = "todo_app/app."
    "MONGODB_CONN" = "${azurerm_cosmosdb_account.main.primary_mongodb_connection_string};"
    "SECRET_KEY" = "${{ secrets.SECRET_KEY }}"
    "OAUTH_CLIENT_ID" = "${{ secrets.OAUTH_CLIENT_ID }}"
    "OAUTH_CLIENT_SECRET" = "${{ secrets.OAUTH_CLIENT_SECRET }}"
    "OAUTHADMIN" = "smellybeagle"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}