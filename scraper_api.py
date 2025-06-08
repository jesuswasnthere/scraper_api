import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/api/p2p-rates")
async def get_binance_p2p_rate():
    try:
        # Hacer la petición HTTP directamente sin Selenium
        url = "https://exchangemonitor.net/venezuela/dolar-binance"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # Descargar la página
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # Verificar errores

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer la tasa de Binance P2P
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
