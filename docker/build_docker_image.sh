sudo docker build -f Dockerfile.paris_windstorm_worker -t coreoasis/model_worker_paris_windstorm:1.26.2 .

sudo docker network create shiny-net

sudo docker-compose -f docker-compose.yml -f docker-compose-paris-windstorm.yml -f docker-compose-ui.yml up -d
