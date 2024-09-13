FROM alpine:3.20.3

WORKDIR /usr/src/app

RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq \
    && echo "Packages Installed."

RUN rm -rf /usr/lib/python3*/EXTERNALLY-MANAGED \
    && pip3 install --force-reinstall -v "bitstring==3.1.9" \
    && echo "Python Packages Installed."

RUN echo 'python3 pretty_j1939.py $1' > run.sh \
    && chmod +x run.sh

COPY pretty_j1939.py .
COPY arg_defaults.py .
COPY pretty_j1939/* ./pretty_j1939/
COPY J1939DA_MAY2022.json .
COPY tmp/temp_2024-09-09.txt .
COPY tmp/can_2024-09-09.txt .
COPY manufacturer.sh .
