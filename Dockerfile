FROM python:3.9.2-slim
COPY requirements.txt /usr
# FIXME: ImportError: libtk8.6.so: cannot open shared object file: No such file or directory
RUN apt-get update && apt-get install python3-tk
RUN pip install -r /usr/requirements.txt
COPY . /usr/brevity-client
WORKDIR /usr/brevity-client
RUN pip install /usr/brevity-client
RUN chmod a+x brevity_client/client.py
CMD ["python3", "brevity_client/client.py"]
