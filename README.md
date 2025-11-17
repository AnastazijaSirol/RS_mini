# AutoMon
Ovaj projekt predstavlja simulacijski sustav za nadzor prometa na autocesti Pula-Rijeka-Umag.
Sustav generira ulaze, izlaze, prolaske kamera i zaustavljanja na odmorištima, a svi se podaci spremaju u lokalnu SQLite bazu traffic.db.

Projekt sadrži i CLI aplikaciju (izrađenu pomoću Typer-a) koja omogućava prikaz statistike i analize podataka. 

## 1. Svrha aplikacije

Aplikacija simulira promet na autocesti Pula-Rijeka-Umag uz praćenje:

Ulaza:

- PULA-ENTRANCE

- RIJEKA-ENTRANCE

- UMAG-ENTRANCE

Izlaza:

- PULA-EXIT

- RIJEKA-EXIT

- UMAG-EXIT

Kamera:

- CAMERA1

- CAMERA2

Odmorišta:

- RESTAREA1

- RESTAREA2

Svi se podaci spremaju u SQLite bazu.

## 2. Način implementacije

Sustav je organiziran u nekoliko modula:

### Skripte simulacija

Svako mjesto na autocesti ima svoju skriptu:

- pula_entrance.py, rijeka_entrance.py, umag_entrance.py

- camera1.py, camera2.py

- pula_exit.py, rijeka_exit.py, umag_exit.py

- restarea1.py, restarea2.py

Svaka skripta radi u petlji i generira simulirane podatke.

### Pohrana podataka

storage.py sadrži:

- inicijalizaciju baze

- funkciju za upis podataka

- funkcije za dohvat podataka

Baza nastaje automatski pri prvom pokretanju.

### CLI aplikacija

cli.py pruža nekoliko naredbi za prikaz statistika i analize podataka:

- broj vozila na određenom ulazu/izlazu
- broj vozila koja su prekoračila brzinu pored određene kamere
- prosječno provedeno vrijeme na određenom odmorištu
- potvrda prekoračenja brzine na temelju ukupnog vremena putovanja

CLI radi direktno nad SQLite bazom.

## 3. Instalacija i priprema okruženja

### Kloniranje projekta

```git clone <repo_url>```

```cd <repo_folder>```

### Kreiranje virtualnog okruženja

```python -m venv venv```

```venv\Scripts\activate```

### Instalacija ovisnosti

```pip install -r requirements.txt```

## 4. Pokretanje sustava naredbom

```python main.py```

## Korištenje CLI sučelja
Svaka se funkcija pokreće zasebno: 

- broj vozila na određenom ulazu/izlazu

```python cli.py count-entrances PULA-ENTRANCE```

```python cli.py count-exits RIJEKA-EXIT```

- broj vozila koja su prekoračila brzinu pored određene kamere

```python cli.py speeding camera1```

- prosječno provedeno vrijeme na određenom odmorištu

```python cli.py avg-rest RESTAREA1```

- potvrda prekoračenja brzine na temelju ukupnog vremena putovanja

```python cli.py fast-travel```

## 5. .exe paket

Projekt sadrži i samostalni .exe paket izrađen pomoću PyInstaller-a.
Ovaj paket omogućuje pokretanje cijelog sustava bez instaliranog Pythona i bez instalacije ovisnosti.

U virtualnom okruženju pokrenuti naredbu: 

```pyinstaller --onefile main.py```

Nakon pokretanja naredbe, izvršna datoteka nalazi se u ```dist/main.exe```