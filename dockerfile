FROM python:3.11
WORKDIR /home/sigeo/defesa_civil_layer_update/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python", "script.py" ]