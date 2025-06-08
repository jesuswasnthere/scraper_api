import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/api/p2p-rates")
async def get_binance_p2p_rate():
    try:
        # Verificar la instalación de Chrome
        chrome_path = shutil.which("google-chrome")
        chromedriver_path = shutil.which("chromedriver")

        if not chrome_path or not chromedriver_path:
            raise RuntimeError("Chrome o ChromeDriver no están instalados correctamente.")

        # Configurar Selenium con Chrome
        chrome_options = Options()
        chrome_options.binary_location = chrome_path  # Indicar la ubicación de Chrome
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Cargar la página
        driver.get("https://exchangemonitor.net/venezuela/dolar-binance")

        # Obtener el HTML actualizado
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Buscar la tasa dentro del div correcto
        rate_section = soup.find("div", class_="history-rate fs-2")

        if rate_section:
            rate_text = rate_section.text.strip().replace("Bs.", "").replace(",", ".")
            rate = rate_text if rate_text else "N/A"

            return {
                "platform": "Binance P2P",
                "rate": rate,
                "last_updated": datetime.now().isoformat()
            }

        return {"error": "Binance P2P rate not found"}

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

# Ejecutar el servidor con Uvicorn en Render
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
