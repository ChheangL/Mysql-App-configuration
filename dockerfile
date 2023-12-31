FROM ubuntu:23.04

WORKDIR /app
# Install app dependencies
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Asia/Bangkok apt -y install python3-pandas
RUN apt -y install python3-flask python3-sqlalchemy python3-pymysql


# Bundle app source
COPY . .

# EXPOSE 5000
CMD [ "python3", "app.py"]