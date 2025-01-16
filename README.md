# RAG Project

This project implements a Retrieval-Augmented Generation (RAG) system using Azure OpenAI, Azure AI Search, Native OpenAI, and Streamlit. The application is deployed as an Azure Web App using GitHub Actions for continuous integration and deployment.

![image](https://github.com/user-attachments/assets/2c9a574c-61ff-421b-b040-df3839c242e6)


## Table of Contents

- [RAG Project](#rag-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Usage](#usage)
  - [Deployment](#deployment)
    - [Using GitHub Actions](#using-github-actions)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

RAG is a technique that combines retrieval-based and generation-based approaches to improve the quality and relevance of generated responses. This project leverages Azure OpenAI and Azure AI Search to implement a robust RAG system, providing enhanced information retrieval and natural language generation capabilities.

## Features

- **Azure OpenAI Integration**: Utilizes Azure OpenAI for advanced natural language processing and generation.
- **Azure AI Search**: Implements Azure AI Search for efficient and accurate information retrieval.
- **Streamlit Interface**: Provides a user-friendly interface using Streamlit for interaction with the RAG system.
- **Continuous Deployment**: Uses GitHub Actions for automated deployment to Azure Web App.

## Architecture

The architecture of the project includes the following components:

1. **Azure OpenAI**: For natural language understanding and generation.
2. **Azure AI Search**: For retrieving relevant documents and information.
3. **Streamlit**: For building the web interface.
4. **Azure Web App**: For hosting the application.
5. **GitHub Actions**: For continuous integration and deployment.

## Setup and Installation

### Prerequisites

- Azure account
- GitHub account
- Python 3.8+
- Streamlit

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/rag-project.git
    cd rag-project
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Azure services:
    - Create an Azure OpenAI resource.
    - Create an Azure AI Search service.
    - Configure the necessary environment variables.

4. Run the Streamlit application locally:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Access the Streamlit interface.
2. Enter your query in the input field.
3. The system retrieves relevant documents using Azure AI Search.
4. Azure OpenAI generates a response based on the retrieved documents.
5. The response is displayed on the Streamlit interface.

## Deployment

### Using GitHub Actions

1. Ensure your repository is connected to GitHub.
2. Set up the GitHub Actions workflow for continuous deployment.
3. Push your changes to the repository.
4. GitHub Actions will automatically deploy the application to Azure Web App.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
