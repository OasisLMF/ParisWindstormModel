sudo docker build -f Dockerfile.paris_windstorm_worker -t paris_windstorm_worker.1_26_2 .

sudo docker network create shiny-net

sudo docker-compose -f docker-compose.yml -f docker-compose-paris-windstorm.yml -f docker-compose-ui.yml up -d
