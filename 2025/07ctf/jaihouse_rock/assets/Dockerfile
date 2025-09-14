FROM python:3.11-slim
WORKDIR /

# In case you are wondering, this is a flag! Might not work in CTFD though :)
ENV FLAG="MDdDVEZ7ZG9uJ3RfcHVuY2hfdGhpc19vbmVfaW5faXRfYWludF90aGF0fQ=="

RUN apt-get update && apt-get install -y \
    curl \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o rockstar.tar.gz https://github.com/RockstarLang/rockstar/releases/download/v2.0.29/rockstar-v2.0.29-linux-x64.tar.gz \
    && tar -xf rockstar.tar.gz --strip-components=1  \
    && rm rockstar.tar.gz

COPY chal.py  /

ENTRYPOINT ["python", "/chal.py"]
