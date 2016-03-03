FROM tykio/tyk-dashboard

RUN apt-get update && \
    apt-get install -y dnsutils

ADD startup /startup
ADD tyk_analytics.conf.template /tyk_analytics.conf.template

CMD ["/startup"]
