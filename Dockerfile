FROM python:alpine

RUN mkdir /var/dns-proxy

WORKDIR /var/dns-proxy

COPY requirements.txt requirements.txt
COPY dns_resolv_bloc.py dns_resolv_bloc.py
COPY boot.sh boot.sh
RUN pip3 install -r requirements.txt
RUN chmod +x boot.sh

EXPOSE 53
ENTRYPOINT ["./boot.sh"]
