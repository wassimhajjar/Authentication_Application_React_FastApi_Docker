from fastapi import FastAPI

app=FastAPI()

@app.get("/health")
def health_check():
    return {"status":"Running..."}

# def main():
#     print("Hello from docker-react-fastapi!")


# if __name__ == "__main__":
#     main()
