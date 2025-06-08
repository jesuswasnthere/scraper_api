from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/api/p2p-rates")
async def get_binance_p2p_rate():
    try:
        # Configurar Selenium con Chrome para entorno sin GUI
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # Requerido en entornos sin servidor
        chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Cargar la página
        driver.get("https://monitordolarvenezuela.com/")

        # Obtener el HTML actualizado
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()  # Cerrar el navegador

        # Extraer la tasa de Binance P2P
        binance_section = soup.find("div", class_="lg:col-span-1 md:col-span3 sm:col-span-3 col-span-4 relative")

        if binance_section:
            rate_tag = binance_section.find("p", class_="font-bold text-xl")
            rate = rate_tag.text.replace("Bs = ", "").replace(",", ".") if rate_tag else "N/A"

            time_date_tags = binance_section.find("small", class_="block").find_all("p") if binance_section.find("small", class_="block") else []
            time = time_date_tags[0].text if len(time_date_tags) > 0 else "N/A"
            date = time_date_tags[1].text if len(time_date_tags) > 1 else "N/A"

            return {
                "platform": "Binance P2P",
                "rate": rate,
                "time": time,
                "date": date,
                "last_updated": datetime.now().isoformat()
            }

        return {"error": "Binance P2P rate not found"}

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

# Ejecutar el servidor con Uvicorn en Vercel
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
