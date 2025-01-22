param location string = resourceGroup().location
param aiSearchServiceName string = 'ai-search-service-${uniqueString(resourceGroup().id)}'
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param aiName string = 'appinsights-${uniqueString(resourceGroup().id)}'
param openAiApiKey string
param githubClientId string
@secure()
param githubClienSecret string

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


resource webAppServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'webappserviceplan-${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'B1' // Basic tier
    tier: 'Basic'
    capacity: 1  // Adjust this if scaling is required
  }
  kind: 'app'
  properties: {
    reserved: true
  }
}


resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2022-11-15' = {
  name: 'cosmosdb-${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
      }
    ]
  }
}

resource cosmosDbDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2022-11-15' = {
  parent: cosmosDbAccount
  name: 'Conversations'
  properties: {
    resource: {
      id: 'Conversations'
    }
  }
  dependsOn: [
    cosmosDbAccount
  ]
}

resource cosmosDbContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2022-11-15' = {
  name: '${cosmosDbAccount.name}/Conversations/Data'
  properties: {
    resource: {
      id: 'Data'
      partitionKey: {
        paths: [
          '/partitionKey'
        ]
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        includedPaths: [
          {
            path: '/*'
          }
        ]
        excludedPaths: [
          {
            path: '/"_etag"/?'
          }
        ]
      }
    }
    options: {
      throughput: 400
    }
  }
  dependsOn: [
    cosmosDbDatabase
  ]
}


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
          value: 'AccountEndpoint=${cosmosDbAccount.properties.documentEndpoint};AccountKey=${cosmosDbAccount.listKeys().primaryMasterKey};Database=Conversations'
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
        { 
          name: 'GITHUB_CLIENT_ID'
          value: githubClientId
        }
        {
          name: 'GITHUB_CLIENT_SECRET'
          value: githubClienSecret
        }
      ]
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      scmMinTlsVersion: '1.2'
      scmIpSecurityRestrictionsDefaultAction: 'Allow'
      ipSecurityRestrictionsDefaultAction: 'Allow'
      pythonVersion: '3.11'
      appCommandLine: 'pip install -r requirements.txt && python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0'
    }
  }
  dependsOn: [
    openAiResource
    searchService
    appInsights
  ]
}


output webAppName string = webApp.name
output searchServiceName string = searchService.name
output cosmosDbName string = cosmosDbAccount.name
output cosmosDbDatabaseName string = cosmosDbDatabase.name
output cosmosDbContainerName string = cosmosDbContainer.name
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output openAiResourceName string = openAiResource.name
output azureOpenAiEndpoint string = openAiResource.properties.endpoint
output aiSearchEndpoint string = aiSearchEndpoint
