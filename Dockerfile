FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    freetds-bin \
    freetds-common \
    freetds-dev


RUN git clone https://github.com/sushantburnawal/sqlgpt/tree/master .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "sqlbase.py", "--server.port=8501", "--server.address=0.0.0.0"]