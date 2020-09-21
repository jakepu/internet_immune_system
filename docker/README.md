##### Clone our repository
`git clone https://github.com/Internet-Data-Analysis/data-pipeline.git`

##### Go to the directory that contains the Dockerfile
`cd docker/` 

##### Build docker image and run docker container

Note: the following is applicable when you want to build a new docker image and start a new docker container. If you want to just use an existing docker container, proceed to the `docker exec` command to enter the container. 

###### Build a docker image based on Dockerfile
`docker build -t internet-immune-system:1.0 .`

###### Start the docker container with the image. The container will be running in the background
`docker run -dit --net=host --name internet-immune-system internet-immune-system:1.0` 

##### Enter the docker container
`docker exec -it internet-immune-system /bin/bash`
