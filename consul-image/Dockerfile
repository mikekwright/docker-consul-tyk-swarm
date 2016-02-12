FROM debian:latest

RUN apt-get update && \
    apt-get install -fy wget unzip && \
    mkdir -p /consul/webui && \
    mkdir -p /consul/app

ADD https://releases.hashicorp.com/consul/0.6.3/consul_0.6.3_web_ui.zip /consul/webui/web_ui.zip
ADD https://releases.hashicorp.com/consul/0.6.3/consul_0.6.3_linux_amd64.zip /consul/app/linux_app.zip
ADD https://get.docker.com/builds/Linux/x86_64/docker-1.9.0 /bin/docker
ADD config.json /etc/consul.d/server/config.json
ADD startup /startup

RUN cd /consul/webui && \
    unzip web_ui.zip && \
    cd /consul/app && \
    unzip linux_app.zip && \
    rm -f /consul/webui/web_ui.zip && \
    rm -f /consul/app/linuz_app.zip
    
EXPOSE 8300 8301 8301/udp 8302 8302/udp 8400 8500 53/udp

CMD ["/startup"]
