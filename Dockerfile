FROM python:latest

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /hhHarvest

COPY . .
RUN pip install --no-cache-dir -r req.txt

#CMD ["python3", "tg_bot.py", "--host", "0.0.0.0", "--port", "80"]
CMD ["python3", "tg_bot.py"]