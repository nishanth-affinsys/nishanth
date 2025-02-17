FROM python:3.9-bullseye AS build-env

ARG INDEX_URL
RUN mkdir -p /root/.config/pip
RUN echo "[global]" >> /root/.config/pip/pip.conf
RUN echo "index-url = $INDEX_URL" >> /root/.config/pip/pip.conf
RUN echo "extra-index-url = https://pypi.org/simple" >> /root/.config/pip/pip.conf

RUN mkdir /backend
RUN mkdir /backend/logs
WORKDIR /backend

COPY requirements.txt /backend/requirements.txt
RUN python -m pip install -r requirements.txt
RUN pip3 install --upgrade pip

# for postgressDB
RUN apt-get update -y && \
    apt-get install libmagic1 libpq-dev libaio1 python3-dev -y --no-install-recommends
RUN apt-get update -y && \
    apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y

# Added Oracle Client 19.6
RUN apt update -y && \
    apt-get install libaio1 -y
RUN mkdir -p /opt/oracle
COPY assets/instantclient_19_6 /opt/oracle/instantclient_19_6
RUN sh -c "echo /opt/oracle/instantclient_19_6 > /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig

COPY . /backend

RUN apt update -y && apt upgrade -y

#distroless
FROM gcr.io/distroless/python3-debian11
COPY --from=build-env --chown=nonroot:nonroot /backend /backend
COPY --from=build-env --chown=nonroot:nonroot /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build-env --chown=nonroot:nonroot /opt/oracle /opt/oracle
COPY --from=build-env --chown=nonroot:nonroot /usr/local/bin /usr/local/bin
COPY --from=build-env --chown=nonroot:nonroot /backend/logs /bot/backend
COPY --from=build-env --chown=nonroot:nonroot /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=build-env --chown=nonroot:nonroot /lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=build-env --chown=nonroot:nonroot /backend/libpython3.9.so.1.0 /usr/lib/x86_64-linux-gnu/


#Run true needed as intermediate container error is being thrown during build stage giving issue in pipeline build
RUN true

#sys env's
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
ENV PYTHONUNBUFFERED=1

#workdir and user nonroot
WORKDIR /backend
USER nonroot


CMD ["/usr/local/bin/gunicorn", "-w", "4", "--bind", "0.0.0.0:8443", "main.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]