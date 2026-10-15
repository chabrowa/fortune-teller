# Jenkins controller with Python and the Docker CLI, for running
# the fortune-teller pipeline locally.
FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI and plugins (buildx, compose) from the official image.
# The Docker daemon itself runs on the host and is reached via the mounted socket.
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker:cli /usr/local/libexec/docker/cli-plugins /usr/local/libexec/docker/cli-plugins