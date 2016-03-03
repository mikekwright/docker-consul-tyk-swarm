FROM debian:latest

RUN apt-get update && \
    apt-get install -fy curl wget unzip && \
    mkdir -p /consul/webui && \
    mkdir -p /consul/app

RUN curl -L https://get.docker.com/builds/Linux/x86_64/docker-1.9.0 -o /bin/docker && \
    cd /consul/webui && \
    curl https://releases.hashicorp.com/consul/0.6.3/consul_0.6.3_web_ui.zip -o /consul/webui/web_ui.zip && \
    unzip web_ui.zip && \
    cd /consul/app && \
    curl https://releases.hashicorp.com/consul/0.6.3/consul_0.6.3_linux_amd64.zip -o /consul/app/linux_app.zip && \
    unzip linux_app.zip && \
    rm -f /consul/webui/web_ui.zip && \
    rm -f /consul/app/linuz_app.zip

#ADD config.json /etc/consul.d/server/config.json
ADD config.server.json /etc/consul.d/server/config.json
ADD config.client.json /etc/consul.d/client/config.json
ADD startup /startup
    
EXPOSE 8300 8301 8301/udp 8302 8302/udp 8400 8500 53 53/udp

CMD ["/startup", "server"]
