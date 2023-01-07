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


You can also start the image as a daemon:

    docker-compose up -d

