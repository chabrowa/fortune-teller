# Jenkins controller with Python, the Docker CLI and kubectl, for running
# the fortune-teller pipeline locally.
FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv curl \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI and plugins (buildx, compose) from the official image.
# The Docker daemon itself runs on the host and is reached via the mounted socket.
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker:cli /usr/local/libexec/docker/cli-plugins /usr/local/libexec/docker/cli-plugins

# kubectl matching the local cluster's minor version (Docker Desktop Kubernetes v1.27)
ARG KUBECTL_VERSION=v1.27.16
RUN curl -fsSLo /usr/local/bin/kubectl \
        "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/$(dpkg --print-architecture)/kubectl" \
    && chmod +x /usr/local/bin/kubectl