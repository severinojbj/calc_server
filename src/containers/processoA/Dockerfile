FROM python

RUN pip install paho-mqtt

ADD ./processoA.py /
ADD ./utils.py /

CMD ["python", "processoA.py"]