<h1 align="center">Bud-core-Analytics-svc</h1> 


## Table of Content

1. [Guide](#guide)
2. [Setup](#setup)
    - [Database Setup and User Creation](#database-setup-and-user-creation)
    - [Starting the Service Server](#starting-the-service-server)
    - [Redis Docker Container](#redis-docker-container)
    - [RabbitMQ Docker Container](#rabbitmq-docker-container)
3. [Features](#features)
    - [SQL Views Generation](#sql-views-generation)
    - [Database Query and Endpoint for Graphs](#database-query-and-endpoint-for-graphs)
    - [Dynamic DB Configuration for Functions](#dynamic-db-configuration-for-functions)
    - [Guide to Making a New Endpoint and Graph](#guide-to-making-a-new-endpoint-and-graph)
4. [Different Containers Deployed](#different-containers-deployed)
    - [Worker](#worker)
    - [Listener](#listener)
    - [Consumer](#consumer)
    - [Main Instance](#main-instance)

## Guide

The Analytics Service is a robust solution designed to handle data permissions, provide endpoints for generating new graphs, execute tailored data queries based on tenant specifications, and seamlessly deliver the queried data to the frontend for rendering purposes.


## Setup

### Database Setup and User creation:
Database supported:
- Postgres
- Oracle
- sqlite

To setup a postgresql connection:

Installation of postgresql
```
apt install postgresql postgresql-contrib
sudo -u postgres psql
```

Creating Database and user: 
```
create database mydb;
create user consoleuser with encrypted password 'buddy124';
grant all privileges on database console to consoleuser;
```

### Starting the service server 
Clone the repository:
```
git clone https://github.com/BankBuddy/bud-core-Analytics-svc.git
cd bud-core-Analytics-svc
```

export your git token
```
export GIT_TOKEN=<your-git-token>
```

Install the dependencies and internal requirements:
```
sh install.sh
```

Set the config and run the server:
```
sh set-env.txt
```

### Redis Docker container
The analytics service requires the redis container to be run at 6378 port.<br> 
To accomplish the same, make sure the docker deamon is running and run the following command:

```
docker rm -f redis && docker run --name redis --network host -d redis
docker exec -it redis redis-cli config set notify-keyspace-events KEA
```

### RabbitMQ docker container
The analytics service requries the queue container to run pub/sub events. 
Execute the following command:
```
docker rm -f queue && docker run --name queue -it --network host -d rabbitmq:3-management
sleep 8
docker exec queue rabbitmqctl add_user buddy buddy
docker exec queue rabbitmqctl set_user_tags buddy administrator
docker exec queue rabbitmqctl set_permissions -p / buddy ".*" ".*" ".*"
docker exec queue rabbitmqctl delete_user guest
```
<hr>

## Features:

### SQL Views Generation

One of the management commands ```setup.py``` helps in generating sql views for different services in case of any failure encountered.  
The command is responsible for creating views in all schemas and can be configured by changing the ```USE_DATABASE_AS_DEFAULT``` and ```tenants``` config variables in ```config.env``` .

### Database Query and Endpoint for Graphs:
Like the name suggests, it prepares the analytics dashboard for different service. It accomplishes the following in the below defined steps:

- The dashboard api is triggered from the console. 
- The API endpoints in the dashboard are called to the analytics service.
- For each endpoint, the corresponding functions are called from the respective django apps. 
- The functions process the request call, queries the data according to any filer specified and returns the data in form of a payload for the next service to render it accordingly.
- The same process is carried for each dashboard. 

Various types of endpoints and their usage: 
1. **Dashboard Views:**  ```/analytics-new/reports/dashboard/<your-dashboard-name>``` 
<br> This will return all the charts, and their details which guides the frontend service on where to render which chart and which end points are to be called.

Example: ```/analytics-new/reports/dashboard/user_behaviour```

Response Received:
```
{
    "chart_title": "User Behaviour",
    "filters": {
        "channel": true,
        "time": true,
        "campaignName": false
    },
    "charts": [
        {
            "type": "table_chart",
            "title": "Top 10 Messages",
            "screenshot": true,
            "color": 0,
            "cols": 6,
            "rows": 1.5,
            "Property": {},
            "description": "The table chart displays the top 10 most frequently exchanged messages between the user and the bot.",
            "chart_api_url": "userbehaviour-charts/top-message/",
            "chart_report_api": "userbehaviour-charts/top_ten_message_export_csv/",
            "chart_report_pdf_api": "userbehaviour-charts/top_ten_message_export_pdf/"
        },
        ...
    ],
    "time_offset": "24",
    "USE_TZ": true
}
```

2. **Channels API** 
<br>This will return all the charts, and their details which guides the frontend service on where to render which chart and which end points are to be called. 

Example: ```/analytics-new/reports/channel```

Response Received:
```
{
    "list_of_values": [
        {
            "display_value": "Webchat",
            "api_value": "webchat"
        },
        ...
        {
            "display_value": "Instagram",
            "api_value": "instagram"
        },
        {
            "display_value": "Whatsapp (Clickatell)",
            "api_value": "whatsappc"
        },
        ...
    ]
}
```

3. **Charts API**   ```/<your-dashboard-name>/<your-chart-endpoint>/``` <br>
This will return all the charts, and their details which guides the frontend service on where to render which chart and which end points are to be called. <br>
Example API Call:
```/bot_daily_top5_handled_msg/?page=1```
<br>Payload Passed:
```
{
  "timestamp__range": [
    "2022-03-22T00:00:00+05:30",
    "2024-03-23T00:00:00+05:30"
  ],
  "channel": [
    "webchat",
    "line",
    "email",
    ... 
  ]
}
```
Response: 
```
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "Message": "hi",
            "count": 123
        },
        {
            "Message": "hello",
            "count": 8
        },
        {
            "Message": "Optout",
            "count": 4
        },
        ...
    ]
}
```
<hr>

## Dynamic DB Configuration for functions

With the introduction of dynamic db for each tenant, there exists a schema for each tenant, to make it simpler to query the data from getting the tenant parameter in the request, there are 2 important functions which helps in configuring the dynamic db. <br>
The ```dynamic_db_connection``` is responsible for establishing the connection to the tenant schema or the main schema based on the ```USE_DATABASE_AS_DEFAULT``` value.
The ```get_db_name``` is used to get the schema name.

Steps to reproduce:

- Import the functions:
    ```from main.utils.dynamic_db import dynamic_db_connection, get_db_name ```
- Add the following before querying data from django ORM: <br>
    ```dynamic_db_connection("<your-service-name")```
- While querying the data, make sure you use: <br>
    ```"db_schema": get_db_name('campaign')```

An example can be seen below:

````
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
def created_campaigns_bignum_generic(request):
    dynamic_db_connection('campaign')
    params = {
        "request": request,
        "models": Campaign,
        "serializers": CampaignSerializer,
        "db_schema": get_db_name('campaign'),
        "count": True,
    }
    return params
````
<hr>

## Guide to making a new endpoint and graph

Throughout the service, one common way has been adopted in order to make queries easier to understand and more generalised. 
Steps to reproduce:
- Import the boiler plate functions <br>
```from main.utils.boiler_plate import get_generic_response```
- While writing the view file:
We return a dictionary from the utils file, where the query parameters are defined in key-value pairs which are later executed by the ```get_generic_response``` function. The view function should be constructed in the way shown below. 
Example shown below:
```
@extend_schema(
    operation_id="list_user_activity",
    tags=[AuthTags.AUTHORIZE],
    description="details of all the actions performed in the console",
)
@action(methods=["POST"], detail=False, url_path="complete_activity_details")
def complete_activity_details(self, request, *args, **kwargs):
    """
    The complete_activity_details function is a generic function that returns the activity details of all activities
        in the database. The function takes in a request object and returns an HTTP response with status code 200 if
        successful, or 400 if unsuccessful.

    :param self: Represent the instance of the object itself
    :param request: Get the request object
    :param *args: Send a non-keyworded variable length argument list to the function
    :param **kwargs: Pass keyworded, variable-length argument list to the function
    :return: A response that contains the following information:
    """
    params = complete_activity_details_generic(request)
    return get_generic_response(params)
```

- The utils file for this view file is responsible for returning the params <br>
Various django orm query parameters can be defined in a key value pair to query and filter the data according to our usage. 
Parameters:

| **Parameter**         | **Description**                                                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------------------------------|
| request(required) | Request body of the API call containing the timestamp, channel, and campaign filters                                  |
| models(required)  | The Django model used for querying the database                                                                       |
| serializers(required) | The serializers responsible for filtering the data according to the request body                                       |
| db_schema(required) | The database schema used to retrieve the data. The value should be `get_db_name("<your-service-name>")`               |
| filter_args (optional) | Used to perform complex filter queries using Q and F objects of Django                                                |
| filter_kwargs (optional) | Used when simple filter queries are to be executed                                                                     |
| exclude (optional) | Used to exclude certain rows based on a condition                                                                      |
| values (optional) | Can be used to group the data by different column names                                                                |
| values_kwargs (optional) | Used to manipulate the field names and their typecasting                                                              |
| annotate (optional) | Used to perform aggregate functions such as min, max, typecasting, etc.                                               |
| order_by (optional) | Used to perform sorting based on a column                                                                              |
| distinct (optional) | Returns the distinct values of a particular column                                                                      |
| count (optional) | Returns the count of the queryset received                                                                             |
| query_set (optional) | Returns the count of distinct values                                                                                    |
| aggregate (optional) | Used to perform aggregate functions such as min, max, etc.                                                             |
| csv_kwargs (optional) | Used when CSV is to be exported through the API                                                                         |
| pdf_kwargs (optional) | Used when PDF is to be exported through the API Call                                                                    |
| not_paginated (optional) | Used when paginated response is to be sent through the API Call                                                        |


Example: 
```
def complete_activity_details_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": Activity,
        "serializers": ActivitySerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "username__isnull": False,
        },
        "annotate": {
            "request_timestamp": Trunc(
                F("request_timestamp"), "second", tzinfo=get_timezone()
            ),
            "timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-timestamp"],
    }
    return params
```

<hr>


## Different Containers Deployed: 

### Worker
The worker container is responsible for executing the CTA Reports which are scheduled every night. 

### Listener
The listener container is responsible for scheduling the CTA reports every night to be executed by the worker container. 

### Consumer
The consumer container handles all the management commands including the SQL views generation

### Main Instance
The main instance is reponsible to run the python server which receives request from the console, check for permissions, query the database, prepare the charts and send the data to the next service.

<hr>

<h4 align="center">End of Document</h4>


<hr>
