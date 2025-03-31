FROM python:3.12.9

WORKDIR /usr/scr/app

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD ["uvicorn", "App.main:app", "--host","0.0.0.0","--port","9000"]