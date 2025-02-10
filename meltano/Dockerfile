ARG MELTANO_IMAGE=meltano/meltano:v2.19.1-python3.10
FROM $MELTANO_IMAGE


RUN useradd -m meltano_user && \
    mkdir -p /project && \
    chown -R meltano_user:meltano_user /project

RUN mkdir -p /data_extraction && \
    chown -R meltano_user:meltano_user /data_extraction

RUN apt-get update && apt-get install -y postgresql-client
USER meltano_user

WORKDIR /project

COPY --chown=meltano_user:meltano_user . .
RUN meltano install

#ENV MELTANO_PROJECT_READONLY 0

ENTRYPOINT ["meltano"]
