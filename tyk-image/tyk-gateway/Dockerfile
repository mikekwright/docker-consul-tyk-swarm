FROM tykio/tyk-gateway:latest

RUN apt-get update && \
    apt-get install -y dnsutils

ADD startup /startup
ADD tyk.conf.template /tyk.conf.template

CMD ["/startup"]

