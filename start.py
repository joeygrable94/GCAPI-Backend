from os import getenv
from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(getenv("BACKEND_PORT", 8888)),
        log_level=getenv("BACKEND_LOG_LEVEL", "info"),
        reload=True
    )
