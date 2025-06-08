import httpx
from bs4 import BeautifulSoup
from datetime import datetime

def get_yadio_rate():
    try:
        # URL de Yadio en Exchange Monitor
        url = "https://exchangemonitor.net/venezuela/dolar-yadio"
        headers = {"User-Agent": "Mozilla/5.0"}

        # Descargar la página
        response = httpx.get(url, headers=headers)
        response.raise_for_status()

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer la tasa de Yadio
        rate_section = soup.find("div", class_="history-rate fs-2")

        if rate_section:
            rate_text = rate_section.text.strip().replace("Bs.", "").replace(",", ".")
            return {
                "platform": "Yadio",
                "rate": rate_text,
                "last_updated": datetime.now().isoformat()
            }

        return {"error": "Yadio rate not found"}

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}
