from tools.cnbis_knowledge_api import app  # noqa: F401 — re-export for uvicorn

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
