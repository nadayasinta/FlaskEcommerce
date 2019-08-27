FROM python:3.6.8
MAINTAINER nadayasinta "nada@alterra.id"
RUN mkdir -p /FlaskEcommerce
COPY . /FlaskEcommerce
RUN pip install -r /FlaskEcommerce/requirements.txt
WORKDIR /FlaskEcommerce
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
