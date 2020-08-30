# coderio

media-coverage
==============

1. [Run using virtualenv](#virtualenvs)
2. [Run using docker](#docker)

#### Install virtualenvwrapper
virtualenvwrapper should be installed into the same 
global site-packages area where virtualenv is installed. 
You may need administrative privileges to do that. The easiest way to install it is using pip

1. Install virtualenvwrapper using pip
	```sh
	sudo pip install virtualenvwrapper
	```

2. Open .bashrc or .zshrc file and add:
	```sh
	# Virtualenvwrapper
	export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 # Optional
	export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv  # Or ~/.local/bin/virtualenv
	export PROJECT_HOME=$HOME/Devel
	export WORKON_HOME=$HOME/Envs
	source /usr/local/bin/virtualenvwrapper.sh  # Or ~/.local/bin/virtualenvwrapper.sh
	```
3. Reload startup file
	```sh
	source ~/.bashrc
	```
	or
	```sh
	source ~/.zshrc
	```

## Configuration
### Create an enviroment
1. Create the environment
	```sh
	cd /path/to/repo/media-coverage
	mkvirtualenv -a . --python=python3 media-coverage
	deactivate
	```
2. Add to `~/Envs/media-coverage/bin/postactivate`:

	```sh
	set -o allexport; source [/path/to/repo/]media-coverage/environments/local; set +o allexport
	export PYTHONPATH=[/path/to/repo/]media-coverage
	```

### Install the requirements
1. Activate the enviroment

	```sh
	workon media-coverage
	```
2. Now install from requirements directory local.txt, libs.txt, production.txt
	```sh
	pip install -r requirements/local.txt
	pip install -r requirements/libs.txt
	pip install -r requirements/production.txt
	```

### Make migrations if needed
```sh
python service/manage.py migrate
```
## Run on 8010 port
```sh
python service/manage.py runserver 8010
```

<div id="docker"></div>
---
# Run locally with docker

### Install Docker and Docker compose
On **Ubuntu 18.x/Debian**
```sh
sudo apt install docker.io
```
Docker Compose:

```sh
sudo apt install docker-compose
```

The Docker service needs to be setup to run at startup. To do so, type in each command followed by enter:

```sh
sudo systemctl start docker
sudo systemctl enable docker

```sh
cd /path/to/repo/media-coverage
mkvirtualenv -a . --python=python3 media-coverage
deactivate
```
Now edit ~/Envs/media-coverage/bin/postactivete
```sh
set -o allexport; source /path/to/repo/media-coverage/environments/local; set +o allexport
export PYTHONPATH=/path/to/repo/media-coverage
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```
>**NOTE:** The credential.json file is provided by the administrator.

```
docker-compose -f containers/compose/docker-compose.yml up
```
If this fails, make sure your user is in the [docker user group](https://docs.docker.com/engine/install/linux-postinstall/) OR run with sudo.
```
