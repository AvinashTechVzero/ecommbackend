From python:3.10 as python
WORKDIR /ecommerce_backend
FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv
RUN export JWT_SECRET_KEY=asd
RUN export JWT_REFRESH_SECRET_KEY=asd1234
RUN nohup poetry run start &
