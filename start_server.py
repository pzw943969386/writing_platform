import uvicorn
from backend.config.setting import settings


def main():
    server_config = settings.server
    uvicorn.run(
        "backend.application:app", host=server_config["ip"], port=server_config["port"]
    )


if __name__ == "__main__":
    main()
