from fastapi import FastAPI, HTTPException
import httpx
import logging
from fastapi.middleware.cors import CORSMiddleware

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {
        "app": "crypto-price",
        "message": "backend is ready",
        "version": "0.1.0"
    }


@app.get("/crypto")
async def get_prices():
    try:
        async with httpx.AsyncClient() as client:
            # Запрос к CoinDesk API для получения текущей цены биткоина
            response_coindesk = await client.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
            response_coindesk.raise_for_status()  # Проверка статуса ответа
            data_coindesk = response_coindesk.json()

            # Запрос к CoinCap API для получения текущей цены эфира
            response_coincap = await client.get("https://api.coincap.io/v2/assets/ethereum")
            response_coincap.raise_for_status()  # Проверка статуса ответа
            data_coincap = response_coincap.json()


            # Запрос к API ЦБ РФ для получения курса доллара к рублю
            response_cbr = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
            response_cbr.raise_for_status()  # Проверка статуса ответа
            data_cbr = response_cbr.json()

            # Получение курса доллара к рублю
            usd_to_rub = data_cbr["Valute"]["USD"]["Value"]

            # Цена биткоина в долларах
            bitcoin_usd = float(data_coindesk["bpi"]["USD"]["rate"].replace(',', ''))

            # Конвертация цены биткоина в рубли
            bitcoin_rub = bitcoin_usd * usd_to_rub

            # Цена эфира в долларах
            ethereum_usd = float(data_coincap["data"]["priceUsd"])

            # Конвертация цены эфира в рубли
            ethereum_rub = ethereum_usd * usd_to_rub

            return {
                "bitcoin": {
                    "usd": bitcoin_usd,
                    "rub": bitcoin_rub
                },
                "ethereum": {
                    "usd": ethereum_usd,
                    "rub": ethereum_rub
                }

            }
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from external API.")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP status error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Error response from external API: {e.response.json()}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Заголовки CORS
origins = [
    "http://localhost:3000"
    "http://127.0.0.1:3000"
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"], )