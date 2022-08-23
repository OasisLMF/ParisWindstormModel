docker build -f Dockerfile.paris_windstorm_worker -t paris_windstorm_worker.1_26_2 .


docker-compose -f docker-compose.yml -f docker-compose-paris-windstorm.yml -f docker-compose-ui.yml up -d
