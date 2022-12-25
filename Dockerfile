FROM registry.xiaoyou.host/nvidia/cuda:torch-1.9.0
USER root
WORKDIR /code
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y  \
    && pip3 install -r requirements.txt -i https://nexus.xiaoyou.host/repository/pip-hub/simple  \
    && python3 setup.py develop
EXPOSE 7001
CMD ["python3","main.py"]