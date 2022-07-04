FROM python

ADD ./test.py /

RUN pip install paho-mqtt

EXPOSE 1883/tcp

CMD ["python", "test.py"]