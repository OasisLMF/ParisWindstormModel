#########
#####
## set of commands to set up an environment for oasislmf
#####
#########

# update env
sudo apt-get update
# install requirements
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# install docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# allow docker to run without sudo
# sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 

# enable docker startup
sudo systemctl enable docker.service
sudo systemctl enable containerd.service

# install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# install pip
sudo apt install -y python3-pip

# set aliases for python and pip
echo "alias python='python3'" >> ~/.bashrc
echo "alias pip='pip3'" >> ~/.bashrc
source ~/.bashrc

# install oasislmf package and dependencies
sudo apt install -y libspatialindex-dev
pip install pip-tools
pip install oasislmf

# adjust path for oasislmf
PATH=$PATH:~/.local/bin

# enable oasislmf autocomplete
oasislmf admin enable-bash-complete -y
source ~/.bashrc



