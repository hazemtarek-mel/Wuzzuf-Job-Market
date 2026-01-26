@echo off
TITLE WUZZUF Market Pulse - Auto Update

echo ========================================================
echo       WUZZUF MARKET PULSE - DAILY UPDATE
echo ========================================================
echo.

echo [1/3] Checking dependencies...
pip install -r requirements.txt
echo.

echo [2/3] Scraping fresh data from Wuzzuf...
python scraper.py
echo.

echo [3/3] Launching Dashboard...
echo (The app will automatically clean and filter the new data)
echo.

streamlit run app.py

pause
