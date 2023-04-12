FROM python:3.8

WORKDIR /workspace

ADD . /workspace

RUN pip install -r requirements.txt

# CMD [ "python" , "/workspace/app.py" ]
# CMD ["gunicorn" "/workspace/app:app"]
ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "app:app"]


RUN chown -R 42420:42420 /workspace

ENV HOME=/workspace
