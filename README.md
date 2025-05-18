# Notatkomator

Projekt Notatkomator – aplikacja do tworzenia notatek, webowo i przez telefon, projekt dokumentowany na YouTube.

[Kanał YouTube](https://www.youtube.com/@CodeByArgan)

# Odpalanie deweloperskie

Polecam stworzyć sobie wirtualne środowisko (virtualenv).  
Aby zainstalować potrzebne biblioteki, wpisujemy: `pip install -r requirements.txt`

Nastepnie skopiuj plik `.env.example` do `.env` i uzupełnij go swoimi danymi.

## Baza danych

Potrzebny jest Docker z Docker Compose. Odpalamy komendą:  
`docker compose -f ./docker-compose.db.dev.yaml up`

Przy pierwszym odpaleniu pamiętaj, aby wykonać inicjalizację Aerich:  
`aerich init-db`

Przy odpalaniu deweloperskim Docker Compose wystawia również Adminera do łatwiejszego zarządzania bazą – login i hasło znajdują się w pliku `docker-compose.db.dev.yaml`.

Nowr migracje towrzymy przy pomocy komendy `aerich migrate --name nazwa_migracji`

## Descope

Aby logownie działało, nalzeży stworzyc sobie konto na Descope i uzupełnić plik `.env` o dane `DESCOPE_ID` w głownym folderze oraz w folderze `ui`.

## Serwer FastAPI

W głównym folderze wpisujemy:  
`uvicorn main:app`  
Podczas developmentu polecam flagę `--reload`, dzięki której serwer będzie odświeżał się automatycznie przy zmianach w plikach.

## Testy

Aby uruchomić testy, wpisujemy:
`PYTHONPATH=. pytest`
