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
async def get_p2p_rates():
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

        # Extraer las secciones P2P
        p2p_sections = soup.find_all("div", class_="lg:col-span-1 md:col-span3 sm:col-span-3 col-span-6 undefined")

        rates = []
        for section in p2p_sections:
            platform_tag = section.find("h3", class_="font-bold")
            platform = platform_tag.text.strip() if platform_tag else "Desconocido"

            rate_tag = section.find("p", class_="font-bold text-xl")
            rate = rate_tag.text.replace("Bs = ", "").replace(",", ".") if rate_tag else "N/A"

            time_date_tags = section.find("small", class_="block").find_all("p") if section.find("small", class_="block") else []
            time = time_date_tags[0].text if len(time_date_tags) > 0 else "N/A"
            date = time_date_tags[1].text if len(time_date_tags) > 1 else "N/A"

            if "Binance P2P" in platform or "El Dorado P2P" in platform:
                rates.append({"platform": platform, "rate": rate, "time": time, "date": date})

        # Agregar última actualización
        rates.append({"last_updated": datetime.now().isoformat()})

        return rates

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

# Ejecutar el servidor con Uvicorn en Vercel
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
