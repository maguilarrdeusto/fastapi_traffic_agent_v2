from fastapi import APIRouter, HTTPException
from app.schemas import OptimizationInput, OptimizationOutput
from app.services.optimization import optimize_kpis

router = APIRouter()

@router.post("/optimize/", response_model=OptimizationOutput)
async def optimize(input_data: OptimizationInput):
    try:
        kpi_results = await optimize_kpis(input_data.data)
        return {"KPIs": kpi_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
