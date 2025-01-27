from os import environ

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=environ.get("API_HOST_IP", "0.0.0.0"),
        port=int(environ.get("API_HOST_PORT", 8888)),
        log_level=environ.get("API_LOG_LEVEL", "info").lower(),
        reload=True,
    )
