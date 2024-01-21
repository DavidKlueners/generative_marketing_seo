## to run chainlit

poetry run chainlit run app.py -w

## to build the Docker image

docker build -t gen-marketing-seo .

### or to build for deploying it on non-ARM architecture

docker buildx build --platform linux/amd64 -t gen-marketing-seo .

## to run the docker image locally

docker run -p 5002:8000 gen-marketing-seo

## to check running docker instances
docker ps

## to shut down instance 
docker stop <container-id>