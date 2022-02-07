FROM python:3

ADD main.py /
ADD HelperFunctions /HelperFunctions
ADD Models /Models

RUN pip install python-binance
RUN pip install numpy
RUN pip install requests

CMD [ "python", "./main.py" ]