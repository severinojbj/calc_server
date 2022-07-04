FROM python

RUN pip install paho-mqtt

ADD ./processoB.py /
ADD ./utils.py /

CMD ["python", "processoB.py"]