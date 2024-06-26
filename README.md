# Social network (Feisubukku)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Website](https://img.shields.io/badge/website-online-green)

## Mô tả ngắn gọn
Đây là 1 dự án nhóm về phát triển 1 trang web mạng xã hội giúp cho mọi người có thể chia sẽ những hình ảnh, câu chuyện dưới dạng bài đăng, người khác có thể tương tác với các bài đăng của mình như bình luận, thả tương tác. Ngoài ra còn có thể kết bạn, nhắn tin, chỉnh sửa trang cá nhân. Dự án còn là nơi chúng tôi luyện tập sử dụng đa cơ sở dữ liệu cùng 1 lúc.

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Điều tâm đắc khi phát triển dự án](#điều-tâm-đắc-khi-phát-triển-dự-án)
- [Demo](#demo)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cài đặt trên Local](#cài-đặt-trên-local)
- [Sử dụng](#sử-dụng)
- [Thông tin liên hệ](#thông-tin-liên-hệ)

## Giới thiệu
Dự án web này được tạo ra để giúp mọi người chia sẻ về cuộc sống của mình. Nó cung cấp các tính năng như
- Đăng ký, đăng nhập xác thực người dùng sửa dụng JWT.
- Đăng bài: người dùng có thể đăng bài kèm nhiều hình ảnh.
- Thả cảm xúc like, haha, ... với bài đăng hoặc comment.
- Comment bài đăng hoặc trả lời comment.
- Kết bạn tìm kiếm bạn bè theo tên.
- Nhận thông báo khi có người gửi lời mời kết bạn, khi có người thả cảm xúc, comment với bài đăng hay comment của mình.
- Nhắn tin thời gian thực
- Chỉnh sửa trang cá nhân

## Điều tâm đắc khi phát triển dự án  
- Cải thiện kỹ năng phát triển web sử dụng ngôn ngữ Python kết hợp framwork Django
- Biết thêm về các loại cơ sở dữ liệu, sử dụng chúng khi nào, vào dự án như nào
- Áp dụng websocket để phát triển tính năng chat realtime
- Thêm kỹ thuật sử dụng Docker
- Biết thêm về triển khai hệ thống cơ sở dữ liệu Master slave của Postgres, Replica set của Mongodb
- Học thêm về Debezium, Kafka để xử lý vấn đề đồng bộ dữ liệu
- Sử dụng Apache Jmeter để test trang web

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

## Cài đặt trên Local

> [!IMPORTANT]
> Cần cài đặt Visualstudio Code, Python, Docker, máy tính RAM >= 16GB

Để cài đặt dự án này, bạn cần làm theo các bước sau:

1. Clone repository:
    ```bash
    git clone https://github.com/ITAnh11/social_network.git
    ```
2. Dùng VSC mở thư mục vừa clone về: 
3. Cài đặt các phụ thuộc cho backend:
    ```bash
    pip install -r requirements.txt
    ```
4. Khởi chạy các service cần thiết trên docker:
    ```bash
    docker-compose up -d
    ```
5. Migrate cho Postgres:
  ```bash
    python manage.py migrate
  ```
6. Cài đặt các trigger, function, ... cho Postgres:  
   6.1 Copy File Dump vào Docker Container
   ```bash
    docker cp database\social_network.sql postgres:/dump.sql
   ```
   6.2 Khôi phục Cơ sở dữ liệu  
   ```bash
    docker exec -it postgres psql -U postgres -d social_network -f /dump.sql
   ```
7. Cài đặt kafka connect:  
   7.1 Sử Postman trên trình duyệt, tạo phương thức POST với url và body raw sau:  
   url
   ```
    localhost:8083/connectors/
   ```
   body
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
   7.2 Có thể xóa connect trên, method DELETE  
   url
   ```
   http://localhost:8083/connectors/pg_connect
   ```

## Sử dụng
Sau khi cài đặt, bạn có thể chạy dự án bằng lệnh sau:

1. Khởi chạy các service trên docker:
    ```bash
    docker-compose up -d
    ```
2. Mở 1 terminal, khởi động server:
    ```bash
    python manage.py runserver
    ```
3. Mở thêm 1 terminal, khởi chương trình động đồng bộ dữ liệu giữa các sở dữ liệu:
    ```bash
    python .\syncdatabase\syncdatabase.py
    ```
4. Trải nghiệm trang web [link](http://127.0.0.1:8000/)

## Thông tin liên hệ
Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ qua email: [buianhkc112004@gmail.com](mailto:buianhkc112004@gmail.com)
