coderio / Ubuntu Setup
==============

1. [Run using virtualenv](#virtualenvs)
2. [Run using docker](#docker) 


<div id="docker"></div>

#### Install virtualenvwrapper
The easiest way to install it is by using pip

1. Install virtualenvwrapper using pip
	```sh
	sudo pip install virtualenvwrapper
	```

2. Open .bashrc or .zshrc file and add:
	```sh
	# Virtualenvwrapper
	export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
	export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv  # Or ~/.local/bin/virtualenv
	export PROJECT_HOME=$HOME/Devel
	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh  # Or ~/.local/bin/virtualenvwrapper.sh
	```
3. Reload startup file
	```sh
	source ~/.bashrc
	```

## Configuration
### Create an enviroment
1. Create the environment
	```sh
	cd /path/to/repo/
	mkvirtualenv --python=python3 coderio
	pip install -r requirements.txt
	deactivate
	```

### Install the requirements
1. Activate the enviroment
	```sh
	workon coderio
	```
2. When accesing the environment, export the PYTHONPATH env variable
	```sh
	export PYTHONPATH=[/path/to/repo/]coderio
	```

### Makemigrations if needed, then
```sh
python service/manage.py migrate
```

### Run on 8010 port
```sh
python service/manage.py runserver 8000
```

<div id="docker"></div>

---
# Run locally with docker

### Install Docker and Docker compose
```sh
sudo apt install docker.io
```

```sh
sudo apt install docker-compose

```
#### Run docker service

```sh
sudo systemctl start docker
sudo systemctl enable docker
```

#### Install Docker and Docker compose

```sh
docker-compose -f docker-compose.yml up
```

If this fails, make sure your user is in the [docker user group](https://docs.docker.com/engine/install/linux-postinstall/) OR run with sudo.
```
