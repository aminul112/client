# Client Async project


## Setup

### Poetry

Make Python virtual environment inside project directory:

    poetry config virtualenvs.in-project true

Install dependencies:

    poetry install

#### Activate the virtual environment

    source .venv/bin/activate


## Building
Make sure Docker is installed and running

### Build docker
    
    docker-compose build 


## Running

### Run docker
Start the image:

    docker-compose up

You can see logs in the console. Log is also saved in the log directory.



## Running Multiple Clients in the same machine

1. Copy source code to another directory.
2. Change CLIENT_PORT and CLIENT_IDENTIFIER values to different values for a separate client example: 6000 and 5678
3. in docker-compose.yml file, change "client:" to something else like "second_client:"
4. in docker-compose.yml file under ports section, 6000:6000
5. Follow the build steps above and you can run as many clients as you want with new port and identifier.
