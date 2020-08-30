coderio / Ubuntu Setup
==============

1. [Run using virtualenv](#virtualenvs)
2. [Run using docker](#docker) 
---
# Run using virtualenv

<div id="docker"></div>

### Install virtualenvwrapper
The easiest way to install it is by using pip

1. Install virtualenvwrapper using pip
	```sh
	sudo pip install virtualenvwrapper
	```

2. Open .bashrc file (it may depend on your distribution) and add:
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
2. When activating the environment, export the following environmental variables
	```sh
	export PYTHONPATH=[/path/to/repo/]coderio
	export DJANGO_SETTINGS_MODULE=coderio.settings
	```
3. (OPTIONAL) If you want to set a specific cache lifetime, export the variable 
CACHE_LIFETIME with the number of days that your cache will last. Default is 3

	```sh
	export CACHE_LIFETIME=10
	```

### Makemigrations if needed, then
```sh
python service/manage.py migrate
```

### Run on 8010 port
```sh
python service/manage.py runserver 8000
```

### Try running endpoints unit tests with
```sh
pytest -vs /star_wars/tests.py
```

<div id="docker"></div>

---
# Run using docker

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

#### Compose Up at root of cloned repo

```sh
docker-compose -f docker-compose.yml up
```

If this fails, make sure your user is in the [docker user group](https://docs.docker.com/engine/install/linux-postinstall/) OR run with sudo.
```
