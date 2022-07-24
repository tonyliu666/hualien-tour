FROM python:3.10-alpine3.16
WORKDIR /app 
RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN python -m pip install pypiwin32
# RUN pip install pyproject-toml
RUN apk add build-base
RUN apk add linux-headers
RUN pip install psutil
# RUN apk add py3-psutil
RUN pip freeze > requirements.txt
COPY requirements.txt .  
RUN pip install -r requirements.txt 
COPY src src 
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 CMD curl -f http://localhost:5000 || exit 1
ENTRYPOINT ["python","./src/main.py"]
