FROM ubuntu:16.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends -y build-essential  \
      git curl ca-certificates python python-setuptools python-pip libssl-dev nano curl
# install github.com/wg/wrk v3.1.0
RUN (mkdir /opt/wrk && cd /opt/wrk && curl -L# https://github.com/wg/wrk/archive/3.1.0.tar.gz | tar zx --strip 1 && make && mv wrk /bin)
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN apt-get clean && apt-get -y remove build-essential curl && apt-get -y autoremove
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . /bookinfo_spec
ARG VCS_REF
ARG BUILD_DATE
# Metadata
LABEL org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/lachie83/k8s-kubectl" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.docker.dockerfile="/Dockerfile"
ENV KUBE_LATEST_VERSION="v1.9.4"
ADD https://storage.googleapis.com/kubernetes-release/release/v1.9.1/bin/linux/amd64/kubectl /usr/local/bin/kubectl
ADD  https://git.io/getLatestIstio  /bookinfo_spec
# RUN export PATH=istio-0.3.0/bin:$PATH
RUN which python
ADD  https://github.com/nginmesh/nginmesh/releases/download/0.6.0/nginmesh-0.6.0.tar.gz /bookinfo_spec
RUN
ENV HOME=/config
RUN set -x && \
    chmod +x /usr/local/bin/kubectl && \
    \
    # Create non-root user (with a randomly chosen UID/GUI).
    adduser kubectl -Du 2342 -h /config && \
    \
    # Basic check it works.
    kubectl version --client
WORKDIR /bookinfo_spec
# CMD ["mamba","--format=documentation ."]
CMD ["tail","-f","/dev/null"]