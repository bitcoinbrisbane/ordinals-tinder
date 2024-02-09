FROM mongo

COPY init.json /init.json
CMD mongoimport --host mongodb --db reach-engine --collection Ordinals --type json --file /init.json --jsonArray