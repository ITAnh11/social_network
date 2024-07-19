# Social network (Feisubukku)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Website](https://img.shields.io/badge/website-online-green)

## Mục lục
- [Demo](#demo)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Deploy](#deploy)
- [Thông tin liên hệ](#thông-tin-liên-hệ)

## Demo
Bạn có thể xem demo trực tuyến của dự án tại: [Demo](https://www.youtube.com/watch?v=CRyd2E1PPxo)

## Công nghệ sử dụng
Dự án này sử dụng các công nghệ sau:
- Frontend: HTML, CSS, Js, Bootraps
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
- Cơ sở dữ liệu: MongoDB, PostgreSQL, Redis
  <p align="left"> 
  <a href="https://redis.io" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="40" height="40"/> </a> 
    <a href="https://www.mongodb.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="40" height="40"/> </a> 
  <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> 
  </p>
- Các công nghệ khác:
  <p align="left"> 
    <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> 
    <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> 
    <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> 
    <a href="https://kafka.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="kafka" width="40" height="40"/> </a> 
    </a> 
  </p>

## Deploy
### Web server
- tạo ec2 (ubuntu)
- connect ec2
- chạy lần lượt các lệnh
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
- set up database Postgres (hướng dẫn tạo postgres ở dưới)
  - migrate database
  ```bash
  python3 manage.py migrate
  ```
  - kết nối tới Postgres, thực thi các lệnh trong file `database/facebook.sql` để tạo các function, trigger....
- Đẩy các file media, static lên S3
  ```bash
  python3 manage.py collecstatic
  ```
### .env
- tạo 1 file .env tương tự file .env.example
- các thông tin thiếu sẽ điền sau khi tạo các dịch vụ ở dưới
- lệnh để gửi lên ec2 web server
  ```bash
  scp -i path\to\key\.pem path\to\.env ubuntu@:Public IPv4 DNS/home/ubuntu/social_network/
  ```
  thay các path\to\key\.pem, path\to\.env, Public IPv4 DNS bằng đường dẫn thực tế

### S3 
[tutorial](https://www.youtube.com/watch?v=JQVQcNN0cXE)
### Mongodb  
[free](https://www.mongodb.com/products/platform/atlas-database)
### Postgres 
[tutorial](https://www.youtube.com/watch?v=z_FN0Zu-Z3Q&t=746s) 
### Redis  
[tutorial](https://www.youtube.com/watch?v=dDwGYGUVTdo)
### Debezium/Kafka 
1. Tạo ec2 (ubuntu)
    > [!IMPORTANT]
    > RAM >= 2GB
2. Connect ec2 chạy lần lượt các lệnh
    ```bash
    sudo apt-get update
    sudo apt-get upgrade

    sudo apt-get install python3-venv
    python3 -m venv env
    source env/bin/activate

    git clone -b deploy https://github.com/ITAnh11/social_network.git
    ```
  3. install docker 
    https://docs.docker.com/engine/install/ubuntu/
  4. Cài đặt debezium, kafka
      ```bash
      cd social_network
      sudo docker-compose up -d
      ```
      check xem có đủ kafka, zookeeper, connect không, nếu không chạy lại lệnh "docker-compose up"
      ```bash
      sudo docker ps
      ```
  5. Tạo connect config 
  - thay thế các chỗ '####' trong file `postgres-connector.json`
  - chạy lệnh 
    ```
    curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
      http://localhost:8083/connectors/ -d @postgres-connector.json
    ```

### Run server
- Connect ec2 Redis 
- Connect ec2 Kafka/Debezium:  vào thư mục dự án 
  ```bash
  sudo docker-compose up -d
  ```
- Connect ec2 web server 1: 
  vào thư mục dự án 
  ```bash
  python3 manage.py runserver 0.0.0.0:8000
  ```
- Connect ec2 web server 2: 
  vào thư mục dự án 
  ```bash
  python3 syncdatabase/syncdatabase.py
  ```

## Thông tin liên hệ
Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ qua email: [buianhkc112004@gmail.com](mailto:buianhkc112004@gmail.com)
