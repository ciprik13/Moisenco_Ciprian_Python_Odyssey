# Real-Time Cryptocurrency Price Prediction

Această aplicație implementează o predicție a prețului criptomonedelor în timp real folosind Streamlit. Aplicația preia prețurile Bitcoin de la API-ul Binance și folosește modelul ARIMA pentru a prezice prețurile viitoare.

## Caracteristici

- Preia prețuri Bitcoin în timp real de la API-ul Binance.
- Utilizează modelul ARIMA pentru a prezice prețurile viitoare.
- Afișează actualizări ale prețurilor în timp real și predicții folosind Streamlit.
- Oferă o reprezentare grafică a prețurilor actuale și prezise.
- Funcție de oprire pentru a încheia aplicația în mod sigur.

## Cerințe

- Python 3.7 sau mai mare
- Trebuie să fie generate API_KEY și API_SECRET de la Binance

## Instalare

1. Clonează acest repozitoriu:

```bash
git clone https://github.com/ciprik13/Moisenco_Ciprian_Python_Odyssey.git
git checkout master
```
2. Crează virtual environment 
```bash
python -m venv .venv
.venv/Scripts/activate.bat
```
3. Adăugarea valorilor de la Binance în .env
   - crează valorile API_KEY și API_SECRET de la Binance

4. Instalează pachetele necesare:

```bash
pip install -r requirements.txt
```

## Rularea aplicației

1. Pentru a porni aplicația Streamlit, rulează::

```bash
streamlit run app.py
```
3. Aplicația se va deschide în browserul tău implicit. Poți vizualiza prețurile Bitcoin în timp real și predicțiile pe interfață. Așteaptă 2 minute.

## Structura proiectului
- app.py: scriptul principal al aplicației.
- requirements.txt: lista pachetelor Python necesare.
- project.log: fișierul de logare pentru înregistrarea evenimentelor aplicației.

## Utilizare
- plicația va prelua continuu cel mai recent preț Bitcoin de la API-ul Binance și va actualiza afișajul prețului. 
- va colecta date despre preț și va folosi modelul ARIMA pentru a prezice prețurile viitoare.
- predicțiile și prețurile actuale sunt reprezentate grafic pentru vizualizare.
- poți opri procesul de preluare a datelor și de predicție prin apăsarea butonului "Stop" de pe interfață.

## Logging
- aplicația înregistrează evenimente importante și erori în project.log pentru depanare și monitorizare.

## Configurație
- creditele API-ului Binance sunt definite în script pentru autentificare.
- poți schimba criptomoneda și valuta împotriva căreia se face predicția modificând variabilele crypto_currency și against_currency în script.
