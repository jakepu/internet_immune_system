# set base image
FROM python:3.6

# set the working directory in the container
WORKDIR /code

<<<<<<< HEAD
# set the volume directory in the container, which is linked to a directory in the host
VOLUME /volume

=======
>>>>>>> origin/data_structure
# copy the dependencies file to the working directory
COPY requirements.txt .

# install (python package)dependencies
RUN ["pip", "install", "-r", "requirements.txt"]

# install desired packages
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "bgpdump"]
