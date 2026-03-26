# OpenAQ-API


Rajapintasovellus datan hakuun tietokannasta


# API-dokumentaatio


Halusin testata API-dokumentaation sisällyttämistä Pythonilla tehtyyn rajapintaan. Tässä käytetään Flasggeria (ilmeisesti Flask + Swagger?)

**API-dokumentaation käytössä on hyödynnetty tekoälyä.** Flasgger-työkalu löytyi seuraavalla promptilla: 

"moi! haluaisin tehdä swaggerin kaltaisen dokumentaation ohjelmalleni. rajapinta hakee dataa postgres tietokannasta ja ohjelma rakennettu pythonilla ja käyttää flask-moduulia tiedonhakuun. mitä erilaisia tapoja on toteuttaa dokumentaatio?" 

Vastauksena -> "

1. Automaattinen dokumentaatio frameworkin kautta
Jos käytät tai voit vaihtaa web-frameworkia, nämä generoivat dokumentaation lähes automaattisesti:
FastAPI — suosituin valinta tähän

Generoi OpenAPI/Swagger-dokuemntaation automaattisesti type hintien perusteella
Sisäänrakennettu Swagger UI ja ReDoc
Ei tarvitse erillistä konfiguraatiota

Flask + flask-smorest tai flasgger

flasgger lisää Swagger UI:n Flask-appiin docstringien tai YAML:n avulla
flask-smorest käyttää marshmallow-schemoja ja generoi OpenAPI-spesin

Django + drf-spectacular tai drf-yasg

Jos käytät Django REST Frameworkia, nämä generoivat dokumentaation automaattisesti
"

Tämän jälkeen annettu prompti: 

"tekisitkö flasgger templaten jotta näen miten se rakennetaan?"

Vastauksena: 

<img width="980" height="1218" alt="image" src="https://github.com/user-attachments/assets/698c390f-0aa8-4338-8b01-8d7c75ce6e61" />

Prompti päättyy tähän. 

## Pohdintaa tekoälyn ehdottomasta Flasggerista
Pienissä projekteissa, kuten tässä Flasggeria voisi hyvin käyttää dokumentoinnin apuvälineenä. On kuitenkin huomioitava, että kun dokumentaatio 
lisätään itse koodiin, niin koodista voi tulla vaikealukuista, koska tiedostossa on sekoitus Pythonia ja yaml-kieltä. Samat toiminnot ovat hyödynnettävissä swagger.io:n kautta.

Saamani template oli selkeä ja siihen oli helppoa tehdä muutoksia, vaikka aluksi yamlin ymmärtäminen tuntui todella haastavalta. Endpointien rakentamisen yhteydessä kieli alkoi
selventyä ja jotkut asiat tuntuivat järkeviltä. Lopulta verrattu tekemiäni flasgger-kuvauksia tähän: https://swagger.io/docs/specification/v3_0/basic-structure/


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

