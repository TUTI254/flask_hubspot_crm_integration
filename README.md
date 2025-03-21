# HubSpot CRM Integration

This project is a simple Flask application that integrates with the HubSpot CRM API.

## Prerequisites

Before running this project, you need to have the following:

- Python 3
- Docker
- Docker Compose

## Installation

1. Clone the repository:

```bash
git clone https://github.com/RYTI254/flask_hubspot_crm_integration.git
```

2. Navigate to the project directory:

```bash
cd flask_hubspot_crm_integration
```

3. Create a `.env` file in the project directory and add the following environment variables based of .env.example:

4. Run the following command to build the application:

```bash
docker-compose build
```

## Usage

To run the application, use the following command:

```bash
docker-compose up
```

This will start the application and expose it on port 5001. eg: http://localhost:5001/


## API DOCS 

Navigate to http://localhost:5001/apidocs/ to view the API documentation.
