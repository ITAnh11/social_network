# Social Network (Feisubukku)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Website](https://img.shields.io/badge/website-online-green)

## Table of Contents
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Contact Information](#contact-information)

## Demo
- You can view the online demo of the project at: [Demo](https://www.youtube.com/watch?v=CRyd2E1PPxo)
- Link online on desciption

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
- Other Technologies:
  <p align="left"> 
    <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> 
    <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> 
    <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 
    <a href="https://kafka.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="kafka" width="40" height="40"/> </a> 
    </a> 
  </p>

## Deployment
### Web Server
1. Create an EC2 instance (Ubuntu).
2. Connect to the EC2 instance.
3. Run the following commands:
  ```bash
  sudo apt-get update
  sudo apt-get upgrade

  sudo apt-get install python3-venv
  python3 -m venv env
  source env/bin/activate

  git clone -b deploy https://github.com/ITAnh11/social_network.git

  cd social_network

  pip install -r requirements.txt
  ```
4. Set up the PostgreSQL database (instructions below):
  - Migrate the database:
  ```bash
  python3 manage.py migrate
  ```
  - Connect to PostgreSQL and execute the commands in the `database/facebook.sql` file to create the necessary functions and triggers.
5. Upload media and static files to S3:
  ```bash
  python3 manage.py collectstatic
  ```

### .env
1. Create a `.env` file similar to `.env.example`.
2. Fill in the missing information after creating the services below.
3. Use the following command to send the `.env` file to the EC2 web server:
  ```bash
  scp -i path\to\key\.pem path\to\.env ubuntu@PublicIPv4DNS:/home/ubuntu/social_network/
  ```
  Replace `path\to\key\.pem`, `path\to\.env`, and `PublicIPv4DNS` with actual paths and DNS.

### S3
Refer to this [tutorial](https://www.youtube.com/watch?v=JQVQcNN0cXE)

### MongoDB  
Refer to [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) for a free setup.

### PostgreSQL 
Refer to this [tutorial](https://www.youtube.com/watch?v=z_FN0Zu-Z3Q&t=746s) 

### Redis  
Refer to this [tutorial](https://www.youtube.com/watch?v=dDwGYGUVTdo)

### Debezium/Kafka 
1. Create an EC2 instance (Ubuntu)
    > **IMPORTANT**
    > Ensure the RAM is at least 2GB.
2. Connect to the EC2 instance and run the following commands:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    git clone -b deploy https://github.com/ITAnh11/social_network.git
    ```
3. Install Docker:
    ```bash
    sudo snap install docker
    ```
4. Set up Debezium and Kafka:
  -  in file `docker-compose.yml` `KAFKA_ADVERTISED_LISTENERS: EXTERNAL_SAME_HOST://#.#.#.#:29092,INTERNAL://kafka:9092` change `#.#.#.#` equal ip of ec2
  - ```
    cd social_network  
    sudo docker-compose up -d
    ```
  - Check if Kafka, Zookeeper, and Connect are running. If not, rerun the `docker-compose up` command:
    ```bash
    sudo docker ps
    ```
6. Create the connector configuration:
  - Replace '####' in the `postgres-connector.json` file.
  - Run the following command:
    ```bash
    curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
      http://localhost:8083/connectors/ -d @postgres-connector.json
    ```

### Run Server
1. Connect to EC2 Redis.
2. Connect to EC2 Kafka/Debezium and run:
  ```bash
  sudo docker-compose up -d
  ```
3. Connect to EC2 Web Server 1 and run:
  ```bash
  python3 manage.py runserver 0.0.0.0:8000
  ```
4. Connect to EC2 Web Server 2 and run:
  ```bash
  python3 syncdatabase/syncdatabase.py
  ```
5. Here's how to use `screen` to run a web server continuously when disconnecting from an EC2 instance:

```bash
# Install `screen` (if not already installed):
sudo apt-get install screen # for Ubuntu/Debian

# Create a new session:
screen -S web_server

# Run your Django server in the `screen` session:
python3 manage.py runserver 0.0.0.0:8000

# Detach from the `screen` session (press Ctrl+A followed by D).

# To reattach to the `screen` session:
screen -r web_server
```
Similarly, you can use this process for running the `syncdatabase` terminal command.

## Contact Information
If you have any questions, please contact via email: [buianhkc112004@gmail.com](mailto:buianhkc112004@gmail.com)
