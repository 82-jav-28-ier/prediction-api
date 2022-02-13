FROM python:3.8-slim

RUN useradd -m myapi

ENV BASE_PATH "/api"

WORKDIR /api


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN chown -R myapi:myapi /api

CMD ["sh", "run.sh"]