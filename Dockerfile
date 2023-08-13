FROM python:latest
COPY ip-daemon.py /
EXPOSE 7777
ENTRYPOINT ["python3", "/ip-daemon.py"]
