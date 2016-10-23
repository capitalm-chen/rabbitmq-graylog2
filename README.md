# rabbitmq-graylog2

## Prerequisites

- Ubuntu 14.04 64bit or newer.
- curl.

```bash
sudo apt-get install curl
```

- Docker.

```bash
curl -sSL https://get.docker.com/ | sudo -E sh
sudo usermod -aG docker $USER
```

Then log in again.

- pip and docker-compose.

```bash
curl -sSL https://bootstrap.pypa.io/get-pip.py | sudo -E python
sudo pip install docker-compose
```

## Running

```bash
cd rabbitmq-graylog2
docker-compose up -d
./configure.sh
```
