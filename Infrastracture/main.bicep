param location string = resourceGroup().location
param aiSearchServiceName string = 'ai-search-service-${uniqueString(resourceGroup().id)}'
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param aiName string = 'appinsights-${uniqueString(resourceGroup().id)}'
param storageAccountName string = 'storage${uniqueString(resourceGroup().id)}'
param cosmosDbName string = 'cosmosdb-${uniqueString(resourceGroup().id)}'
param openAiApiKey string

var openAiKeys = openAiResource.listKeys()
var searchAdminKeys = searchService.listAdminKeys()
var aiSearchEndpoint = 'https://${searchService.name}.search.windows.net'

resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: aiSearchServiceName
  location: location
  sku: {
    name: 'free'
  }
  properties: {
    hostingMode: 'default'
    partitionCount: 1
    replicaCount: 1
  }
}

resource openAiResource 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'openai-${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'S0' // Standard SKU
  }
  kind: 'OpenAI'
  properties: {
    apiProperties: {
      enableOpenAI: true
    }
    customSubDomainName: 'openai-${uniqueString(resourceGroup().id)}'
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

resource webAppServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'webappserviceplan-${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'F1' // Free tier
    tier: 'Free'
  }
  kind: 'app'
  properties: {
    reserved: true
  }
}

// resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2022-11-15' = {
//   name: cosmosDbName
//   location: location
//   kind: 'GlobalDocumentDB'
//   properties: {
//     databaseAccountOfferType: 'Standard'
//     locations: [
//       {
//         locationName: location
//       }
//     ]
//   }
// }

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: aiName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: webAppServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'COSMOS_DB_CONNECTION_STRING'
          value: 'cosmosDbAccount.listKeys().primaryMasterKey'
        }
        {
          name: 'DATABASE_NAME'
          value: 'Conversations'
        }
        {
          name: 'CONTAINER_NAME'
          value: 'Data'
        }
        {
          name: 'OPENAI_API_KEY'
          value: openAiApiKey
        }
        {
          name: 'AZURE_OPENAI_API_KEY'
          value: openAiKeys.key1
        }
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: openAiResource.properties.endpoint
        }
        {
          name: 'AZURE_AI_SEARCH_ENDPOINT'
          value: aiSearchEndpoint
        }
        {
          name: 'AZURE_AI_SEARCH_API_KEY'
          value: searchAdminKeys.primaryKey
        }
        {
          name: 'AZURE_AI_SEARCH_INDEX_NAME'
          value: 'rag-test-oo1'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
      ]
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
    }
  }
}

output webAppName string = webApp.name
output searchServiceName string = searchService.name
output cosmosDbName string = 'cosmosDbAccount.name'
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output openAiResourceName string = openAiResource.name
output azureOpenAiEndpoint string = openAiResource.properties.endpoint
output aiSearchEndpoint string = aiSearchEndpoint
