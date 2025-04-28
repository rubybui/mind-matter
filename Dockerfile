# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=3.12         
FROM python:${INSTALL_PYTHON_VERSION}-slim-bullseye AS builder


WORKDIR /app

COPY requirements requirements
RUN pip install --no-cache -r requirements/prod.txt

COPY mind_matter_api mind_matter_api

COPY .env.example .env

# ================================= PRODUCTION =================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-bullseye as production

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

COPY . .

ENV PORT = 8080
EXPOSE 8080
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]
