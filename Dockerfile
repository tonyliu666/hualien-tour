FROM python:3.10.0-alpine3.15
WORKDIR /app
# RUN python -m pip install pypiwin32
# RUN pip install flask      
# RUN apk add py3-psutil
# RUN pip freeze > requirements.txt
COPY . . 
RUN python -m venv myproject
# ENTRYPOINT ../../app/myproject/Scripts/activate
# CMD ["Activate.ps1","/app/Scripts"]
RUN source myproject/bin/activate
RUN apk add build-base 
# RUN apk add curl 
RUN apk add curl unzip libexif udev chromium chromium-chromedriver xvfb && \
	pip install selenium && \
	pip install pyvirtualdisplay
RUN apk add linux-headers
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r web/requirements.txt 
RUN pip install flask 
RUN pip install psycopg2-binary
HEALTHCHECK --interval=5s --timeout=5s --start-period=30s --retries=3 CMD curl --fail localhost || exit 1
# ENTRYPOINT ["python","/app/src/main.py"]
