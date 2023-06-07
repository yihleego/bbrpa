docker stop rpa
docker rm   rpa
docker rmi  rpa

docker build -t rpa .
docker run -d -it -p 18000:18000 --name=rpa rpa