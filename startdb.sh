#! /usr/bin/sh

docker build -t mydatabase mydata/.
docker build -t phpmyadmin1 phpApp/.

docker run -d --name=myDB -v ./mydata:/config -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro -p 5001:3306 --restart unless-stopped mydatabase

docker run --name phpmyadmin -d --link myDB:db -p 80:80 --restart unless-stopped phpmyadmin1

docker run -d --name=myweb -p 5005:5005 --restart unless-stopped lychheang008/my_web_flask:2.0