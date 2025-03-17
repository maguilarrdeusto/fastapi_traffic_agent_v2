from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes import optimize
import os

app = FastAPI(title="Traffic LLM API", description="API para optimización de tráfico")

# Incluir las rutas correctamente
app.include_router(optimize.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API de optimización de tráfico en FastAPI"}

# Manejar la petición del favicon.ico para evitar el error 404
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    icon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    return FileResponse(icon_path) if os.path.exists(icon_path) else {"detail": "No favicon found"}
