sudo docker build -f docker/Dockerfile.paris_windstorm_worker -t coreoasis/model_worker_paris_windstorm:1.26.2 .

sudo docker pull coreoasis/oasisui_app:1.11.3

sudo docker network create shiny-net

sudo docker-compose -f docker/docker-compose.yml -f docker/docker-compose-paris-windstorm.yml -f docker/docker-compose-ui.yml up -d
