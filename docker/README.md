### Enter the docker container
You can enter a running docker container via the following command:

`docker exec -it internet-immune-system /bin/bash`

This will satisfy most use cases. If you want to rebuild the docker image and the container, refer to the following.

### Build docker image and run docker container 

#### Clone our repository
`git clone https://github.com/Internet-Data-Analysis/data-pipeline.git`

#### Go to the directory that contains the Dockerfile
`cd data-pipeline/docker/` 

Make the desired changes to the Dockerfile:

`vi Dockerfile`

#### Build a docker image based on updated Dockerfile
`docker build -t internet-immune-system:[xxx] .`

#### Start the docker container with the new image.
Run the following command to kick of a new docker container, where `internet-immune-system:[xxx]` corresponds to the tag of the new image we just created:

`docker run -dit --volume=/home/proj_internetml/volume:/volume --net=host --name internet-immune-system internet-immune-system:[xxx]` 

Note that the container will be running in the background. Also note that here we set the volume directory in the container, so that the `/home/proj_internetml/volume` directory on the host is mounted to `/volume` in the docker container 

#### Enter the docker container

`docker exec -it internet-immune-system /bin/bash`
