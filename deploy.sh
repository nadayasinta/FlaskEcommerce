sudo docker stop flaskecommerce
sudo docker rm flaskecommerce
sudo docker rmi nadayasinta/flaskecommerce:latest
sudo docker run -d --name flaskecommerce -p 5000:5000 nadayasinta/flaskecommerce:latest
