FROM python:3.9-slim-buster
RUN mkdir -p /app/state_storage
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt
ADD . .
ENV MONGODB_URI=mongodb://hds:PvU3oaGvwqocVQu7wa3rdplvnHS2ZOJJ@172.27.226.72:27017
ENV MONGO_DATABASE=dartil-main
ENV AWS_HOST=172.27.226.72:9000
ENV S3_HOST=http://172.27.226.72:9000/
ENV AWS_ACCESS=hds
ENV AWS_SECRET=z2hfA87pjgcqqWNNC6010PAYhg0zhMos
ENV BUCKET_NAME=dartil-main
ENV PROXY_PROVIDER=172.27.226.11
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV STATE_KEYNAME=dartil_0
ENV BOTTLE_NECK=5
ENV LOCAL=False
ENV SLEEPING=3

#docker run --network vortex --name gheymat-category --log-driver local --log-opt max-size=2m --log-opt max-file=2 -d gheymat:category
ENTRYPOINT ["python3.9", "main.py"]
