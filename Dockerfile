FROM nginx/unit:1.26.1-python3.9
WORKDIR /бот
COPY . .
#RUN --mount=type=cache,target=/cache-build/ pip install -r /clasificator/requirements.txt
RUN pip install -r /бот/requirements.txt
COPY ./nginx_config.json /docker-entrypoint.d/nginx_config.json
ENV PYTHONPATH /бот
#ENV TRANSFORMERS_CACHE=/clasificator/cache
#ENV HF_HOME=/clasificator/cache
EXPOSE 8081 
RUN chmod -R 777 /root/
CMD ["unitd","--no-daemon","--control", "unix:/var/run/control.unit.sock"]