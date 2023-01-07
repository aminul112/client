
Make sure poetry is installed properly in your build system.

Make Python virtual environment inside project directory
poetry config virtualenvs.in-project true

Install all modules locally
poetry install

Activate Python virtual environment
source .venv/bin/activate 

Build docker container
docker-compose build 

Run Docker container
docker-compose up
