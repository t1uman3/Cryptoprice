from fastapi import FastAPI, HTTPException
import httpx
import logging
from fastapi.middleware.cors import CORSMiddleware
from settings import API_KEY_COINMARKETCAP

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
            # Запрос к CoinMarketCap API для получения цен криптовалют Bitcoin, Ethereum и TON
            headers = {
                'X-CMC_PRO_API_KEY': API_KEY_COINMARKETCAP,
            }
            response_coinmarketcap = await client.get(
                "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,TON",
                headers=headers
            )
            response_coinmarketcap.raise_for_status()
            data_coinmarketcap = response_coinmarketcap.json()

            # Запрос к API ЦБ РФ для получения курса доллара к рублю
            response_cbr = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
            response_cbr.raise_for_status()
            data_cbr = response_cbr.json()

            # Получение курса доллара к рублю
            usd_to_rub = data_cbr["Valute"]["USD"]["Value"]

            # Получение цен криптовалют
            bitcoin_usd = float(data_coinmarketcap["data"]["BTC"]["quote"]["USD"]["price"])
            ethereum_usd = float(data_coinmarketcap["data"]["ETH"]["quote"]["USD"]["price"])
            ton_usd = float(data_coinmarketcap["data"]["TON"]["quote"]["USD"]["price"])

            # Конвертация в рубли
            bitcoin_rub = bitcoin_usd * usd_to_rub
            ethereum_rub = ethereum_usd * usd_to_rub
            ton_rub = ton_usd * usd_to_rub

            return {
                "bitcoin": {
                    "usd": bitcoin_usd,
                    "rub": bitcoin_rub
                },
                "ethereum": {
                    "usd": ethereum_usd,
                    "rub": ethereum_rub
                },
                "ton": {
                    "usd": ton_usd,
                    "rub": ton_rub
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