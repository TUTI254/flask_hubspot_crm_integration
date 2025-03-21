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

4. Run the following command to Build and run the application using Docker Compose:

```bash
docker-compose up --build
```
This will start the application and expose it on port 5001. eg: http://localhost:5001/

## Usage

Once the application is running, you can interact with it using the following endpoints:

Base URL
All endpoints are prefixed with /api/v1.

## Base Endpoints
All endpoints are prefixed with /api/v1.

## API Endpoints

Navigate to http://localhost:5001/apidocs/ to view the API documentation.

## 1. Fetch New CRM Objects
#### Endpoint: GET /new-crm-objects

Description: Fetches new contacts, deals, and tickets with pagination support.

Query Parameters:
```
page: Page number (default: 1).

limit: Number of items per page (default: 10).
```
##  2. Create or Update a Contact
#### Endpoint: POST /contacts

Description: Creates or updates a contact in HubSpot and saves it to the database.

Required Fields:
```
email (string)

firstname (string)

lastname (string)

phone (string)
```
## 3. Create or Update a Deal
#### Endpoint: POST /deals

Description: Creates or updates a deal in HubSpot and saves it to the database.

Required Fields:
```
dealname (string)

amount (number)

dealstage (string)

contact_id (integer)
```
## 4. Create a Support Ticket
#### Endpoint: POST /tickets

Description: Creates a new support ticket in HubSpot and saves it to the database.

Required Fields:
```
subject (string)

description (string)

category (string)

pipeline (string)

hs_ticket_priority (string)

hs_pipeline_stage (string)

contact_id (integer)

deal_ids (array of integers, optional)
```

## API DOCS
    The API is documented using Swagger UI. To access the documentation:
Start the application using docker-compose up.

Navigate to: `http://localhost:5001/apidocs/`

## Video Overview
this is  a short recording illustrating the breakdown of task and the Project overview based on folder structure: https://www.loom.com/share/7092c195a37347df88c8e6cebf448b07
