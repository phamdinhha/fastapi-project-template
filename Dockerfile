FROM python:3.12.7-alpine3.20
ENV TZ=Asia/Ho_Chi_Minh
WORKDIR /app

RUN apk add --no-cache \
    libgcc \
    libc6-compat \
    libstdc++ \
    zip \
    unzip \
    build-base \
    py3-pip

RUN apk add busybox --upgrade
RUN apk add krb5 --upgrade
RUN apk add py3-pip --upgrade

WORKDIR /app
RUN pip install --progress-bar off --upgrade pip
RUN pip install --progress-bar off virtualenv
COPY requirements.txt /app/
RUN virtualenv .venv
ENV VIRTUAL_ENV /app/.venv
ENV PATH /app/.venv/bin:$PATH
RUN which python
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip==24.0.0
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
