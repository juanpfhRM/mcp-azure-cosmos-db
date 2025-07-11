from src.app_init import init_app
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)