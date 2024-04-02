ARG base_image=python:3.10-alpine

FROM ${base_image} AS build

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

FROM ${base_image}


COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /
COPY ./product_api_service /product_api_service

EXPOSE 5000

CMD ["gunicorn", "--reload", "-w", "3", "-b", "0.0.0.0:5000", "product_api_service:create_app()", "--access-logfile", "-"]
