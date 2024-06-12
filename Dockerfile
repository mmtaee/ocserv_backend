FROM ubuntu:24.04

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update

RUN apt install -y --no-install-recommends ocserv gnutls-bin build-essential

RUN apt install -y --no-install-recommends iptables sudo openssl

RUN apt install -y --no-install-recommends python3 python3-pip python3-venv

RUN echo net.ipv4.ip_forward=1 | tee -a /etc/sysctl.conf && sysctl -p

RUN cd /opt && python3 -m venv venv

WORKDIR /app

COPY requirements.txt .

RUN  . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./configs/ocserv.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /etc/ocserv

EXPOSE 443/tcp 443/udp

ENTRYPOINT ["/entrypoint.sh"]
