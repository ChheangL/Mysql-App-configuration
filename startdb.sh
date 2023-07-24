#! /usr/bin/sh

docker build -t mydatabase mydata/.
docker build -t phpmyadmin1 phpApp/.

docker run -d --name=myDB -v ./mydata:/config -p 5001:3006 --restart unless-stopped mydatabase

docker run --name phpmyadmin -d --link myDB:db -p 8080:80 phpmyadmin1
