# OpenAQ-API
Rajapintasovellus datan hakuun tietokannasta

# API-dokumentaatio

Halusin testata API-dokumentaation sisällyttämistä Pythonilla tehtyyn rajapintaan. Tässä käytetään Flasggeria (ilmeisesti Flask + Swagger?)

Kun rajapinta on käynnissä, liitä selaimeen http://127.0.0.1:5000/apidocs/

# Endpointit

## Yhden päivän mittaukset
GET /measurements/<location_id>/day/<day>

Esim: /measurements/2992/day/2020-01-01

## Mittausten kokonaislukumäärä
GET /measurements/<location_id>/count

Esim: /measurements/2992/count

## Päivittäinen keskiarvo
GET /measurements/<location_id>/daily-avg?day=<day>&parameter=<parameter>

Esim: /measurements/2992/daily-avg?day=2020-01-01&parameter=pm10

# Testauksen endpointit

## Listaa kaikki mittauspisteet
GET /test

## Tarkista tietokannassa olevat päivämäärät
GET /test2
