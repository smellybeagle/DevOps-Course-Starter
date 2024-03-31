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

data "azurerm_resource_group" "test" {
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
  shard_key           = "uniqueKey"
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
    "DOCKER_REGISTRY_SERVER_URL" = "https://docker.io"
    "WEBSITES_PORT" = "8000"
    "FLASK_APP" = "todo_app/app."
    "MONGODB_CONN" = "mongodb://${azurerm_cosmosdb_account.main.primary_mongodb_connection_string};"
    "SECRET_KEY" = "${var.SECRET_KEY}"
    "OAUTH_CLIENT_ID" = "${var.OAUTH_CLIENT_ID}"
    "OAUTH_CLIENT_SECRET" = "${var.OAUTH_CLIENT_SECRET}"
    "OAUTHADMIN" = "smellybeagle"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}


# Create App Service Plan
resource "azurerm_service_plan" "test" {
  name                = "test-smellybeagle-asp"
  location            = data.azurerm_resource_group.test.location
  resource_group_name = data.azurerm_resource_group.test.name
  os_type             = "Linux"
  sku_name            = "B1"
}


resource "azurerm_cosmosdb_account" "test" {
  name                = "test-effybeagle"
  location            = data.azurerm_resource_group.test.location
  resource_group_name = data.azurerm_resource_group.test.name
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

data "azurerm_cosmosdb_account" "test" {
  name = "test-effybeagle"
  depends_on = [azurerm_cosmosdb_account.test]
  resource_group_name = data.azurerm_resource_group.test.name
}

resource "azurerm_cosmosdb_mongo_database" "test" {
  name                = "todo_app"
  depends_on = [azurerm_cosmosdb_account.test]
  resource_group_name = data.azurerm_resource_group.test.name
  account_name        = azurerm_cosmosdb_account.test.name
}



resource "azurerm_cosmosdb_mongo_collection" "test" {
  name                = "todolist"
  depends_on = [azurerm_cosmosdb_mongo_database.test]
  resource_group_name = data.azurerm_resource_group.test.name
  account_name        = azurerm_cosmosdb_account.test.name
  database_name       = azurerm_cosmosdb_mongo_database.test.name
  default_ttl_seconds = "777"
  shard_key           = "uniqueKey"
    index {
    keys   = ["_id"]
    unique = true
  }
}
# Create New Web App
resource "azurerm_linux_web_app" "test" {
  name                = "test-smellybeagle-app"
  location            = data.azurerm_resource_group.test.location
  resource_group_name = data.azurerm_resource_group.test.name
  service_plan_id     = azurerm_service_plan.test.id

  site_config {
    application_stack {
      docker_image     = "lvarnham/smellybeagle"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://docker.io"
    "WEBSITES_PORT" = "8000"
    "FLASK_APP" = "todo_app/app."
    #"TEST_MONGODB_CONN" = "${output.TEST_MONGODB_CONN}"
    "TEST_MONGODB_CONN" = "mongodb://${azurerm_cosmosdb_account.test.primary_mongodb_connection_string};"
    "SECRET_KEY" = "${var.TEST_SECRET_KEY}"
    "OAUTH_CLIENT_ID" = "${var.TEST_OAUTH_CLIENT_ID}"
    "OAUTH_CLIENT_SECRET" = "${var.TEST_OAUTH_CLIENT_SECRET}"
    "OAUTHADMIN" = "smellybeagle"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}