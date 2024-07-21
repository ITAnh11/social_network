# Social Network (Feisubukku)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Website](https://img.shields.io/badge/website-online-green)

## Short Description
This is a group project for developing a social network website that allows users to share images and stories in the form of posts. Others can interact with these posts through comments and reactions. Additionally, users can make friends, chat, and edit their profiles. The project also serves as a platform for us to practice using multiple databases simultaneously.

## Table of Contents
- [Introduction](#introduction)
- [Lessons Learned from the Project](#lessons-learned-from-the-project)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Local Installation](#local-installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contact Information](#contact-information)

## Introduction
This web project was created to help people share their lives. It provides features such as:
- User registration and authentication using JWT.
- Posting: users can create posts with multiple images.
- Reacting to posts and comments with emotions like like, haha, etc.
- Commenting on posts or replying to comments.
- Making friends and searching for friends by name.
- Receiving notifications when someone sends a friend request, reacts to, or comments on their posts or comments.
- Real-time messaging.
- Editing user profiles.

## Lessons Learned from the Project
- Improved web development skills using Python with the Django framework.
- Gained knowledge about different types of databases and their appropriate usage in projects.
- Applied websocket for developing real-time chat features.
- Learned how to use Docker.
- Gained knowledge about the master-slave database system of Postgres and the Replica set of MongoDB.
- Learned about Debezium and Kafka for data synchronization.
- Used Apache Jmeter for web testing.

## Demo
You can view the online demo of the project at: [Demo](https://www.youtube.com/watch?v=CRyd2E1PPxo)  
You can experience it live at link on description.

## Technologies Used
This project uses the following technologies:
- Frontend: HTML, CSS, JS, Bootstrap
  <p align="left"> 
   <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> 
    <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a>
   <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> 
     <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a> 
  </p>
- Backend: Python, Django
  <p align="left"> 
  <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> 
    <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> 
  </p>
- Databases: MongoDB, PostgreSQL, Redis
  <p align="left"> 
  <a href="https://redis.io" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="40" height="40"/> </a> 
    <a href="https://www.mongodb.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="40" height="40"/> </a> 
  <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> 
  </p>
- Other technologies:
  <p align="left"> 
    <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> 
    <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> 
    <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 
    <a href="https://kafka.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="kafka" width="40" height="40"/> </a> 
    </a> 
  </p>

## Local Installation

> **IMPORTANT**
> You need to install Visual Studio Code, Python, Docker, and have a computer with at least 16GB RAM.

To install this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/ITAnh11/social_network.git
    ```
2. Open the cloned folder using VSC:
3. Install dependencies for the backend:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the necessary services on Docker:
    ```bash
    docker-compose up -d
    ```
5. Migrate the database for Postgres:
  ```bash
    python manage.py migrate
  ```
6. Set up triggers, functions, etc., for Postgres:  
   6.1 Copy the dump file into the Docker container
   ```bash
    docker cp database/social_network.sql postgres:/dump.sql
   ```
   6.2 Restore the database  
   ```bash
    docker exec -it postgres psql -U postgres -d social_network -f /dump.sql
   ```
7. Set up Kafka Connect:  
   7.1 Use Postman on the browser, create a POST method with the following URL and raw body:  
   URL
   ```
    localhost:8083/connectors/
   ```
   Body
   ```
     {
      "name": "pg_connect",
      "config": {
          "topic.prefix": "social_network",
          "database.hostname": "postgres",
          "database.port":"5432",
          "database.user": "postgres",
          "database.password": "postgres",
          "database.dbname": "social_network",
          "table.include.list": "public.users_user,public.userprofiles_userprofile,public.userprofiles_imageprofile",       
          "query.fetch.size": 500,
          "topic.creation.groups": "debezium-etl",
          "topic.creation.debezium-etl.include": "",
          "topic.creation.debezium-etl.exclude": "",
          "topic.creation.default.partitions": -1,
          "topic.creation.default.replication.factor": -1,
          "plugin.name": "pgoutput",
          "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
          "tasks.max": "1",
          "skipped.operations": "r",
          "snapshot.mode": "never",
          "slot.name": "debezium",
          "publication.autocreate.mode": "filtered",
          "publication.name": "dbz_publication",
          "transforms": "unwrap",
          "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
          "transforms.unwrap.add.fields": "op,ts_ms,source,after, before"
      }
    }
   ```
   7.2 To delete the above connector, use the DELETE method  
   URL
   ```
   http://localhost:8083/connectors/pg_connect
   ```

## Usage
After installation, you can run the project with the following commands:

1. Start the services on Docker:
    ```bash
    docker-compose up -d
    ```
2. Open a terminal and start the server:
    ```bash
    python manage.py runserver
    ```
3. Open another terminal and start the data synchronization program between the databases:  
    ```bash
    python ./syncdatabase/syncdatabase.py
    ```
4. Experience the website [local link](http://127.0.0.1:8000/)

## Deployment
To learn how to deploy, switch to the [`deploy`](https://github.com/ITAnh11/social_network/tree/deploy) branch.

## Contact Information
If you have any questions, please contact via email: [buianhkc112004@gmail.com](mailto:buianhkc112004@gmail.com)
