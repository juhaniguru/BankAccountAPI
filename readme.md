# Asennus

## Ennakkovaatimukset
- tarvitset Postgresin
- kopioi .env.example
- nimeä kopio .env:ksi
- muuta muuttujien arvot .env-tiedostossa vastaamaan omaa Postgres-palvelintasi

## Luo virtualenv

- python -m venv .venv

## Aktivoi virtualenv

### Windows

- .\.venv\Scripts\activate

### Mac / Linux

- source ./.venv/bin/activate

## Asenna riippuvuudet

- python -m pip install -r requirements.txt

## Vie data tietokantaan

### Suorita init_db

- python init_db.py
- suorita vaihtoehdot 1-5

###  Suorita api.py

- python api.py
