import uvicorn


def main():
    uvicorn.run("backend.application:app", host="0.0.0.0", port=8888)


if __name__ == "__main__":
    main()
