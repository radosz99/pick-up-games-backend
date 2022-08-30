docker stop $(docker ps -q --filter ancestor=pug_backend)
docker build -t pug_backend .
docker run -d -p 8121:8121 pug_backend