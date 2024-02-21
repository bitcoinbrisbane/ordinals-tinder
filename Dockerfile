# FROM mongo

# COPY init.json /init.json
# CMD mongoimport --host mongodb --db reach-engine --collection Ordinals --type json --file /init.json --jsonArray

FROM python:3.10
WORKDIR /root/ordinals-tinder/backend/src
COPY . .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
