import time
import httpx
from app.config import settings

async def calculate_kpis(weights: dict) -> dict:
    # Normalizar los pesos si su suma es mayor a 1
    total_weight = sum(weights.values())
    if total_weight > 1:
        weights = {k: v / total_weight for k, v in weights.items()}
    
    # Cálculo de los KPI baseline con multiplicadores fijos
    baseline = {
        "PT Frequency": weights["weight_PublicTransport"] * 54.925,  # 0.4 * 54.925 ≈ 21.97
        "PT Delay": weights["weight_PublicTransport"] * 442.28,      # 0.4 * 442.28 ≈ 176.91
        "Operational Cost": weights["weight_OperationalCost"] * 0.353,  # 0.15 * 0.353 ≈ 0.05312
        "Congestion (Delay)": weights["weight_Congestion"] * 0.86,     # 0.3 * 0.86 ≈ 0.258
        "Emissions": weights["weight_Emissions"] * 0.00786,            # 0.15 * 0.00786 ≈ 0.001179
    }
    baseline["System Cost"] = 468.38604563398485

    # Cálculo de los KPI optimizados con otros multiplicadores fijos
    optimized = {
        "PT Frequency": weights["weight_PublicTransport"] * 47.05882352941177,  # 0.4 * 47.05882 ≈ 18.82353
        "PT Delay": weights["weight_PublicTransport"] * 390.2118247886935,       # 0.4 * 390.21182 ≈ 156.08473
        "Operational Cost": weights["weight_OperationalCost"] * 0.41678,         # 0.15 * 0.41678 ≈ 0.06251685
        "Congestion (Delay)": weights["weight_Congestion"] * 1.00409,            # 0.3 * 1.00409 ≈ 0.30122784
        "Emissions": weights["weight_Emissions"] * 0.00776,                      # 0.15 * 0.00776 ≈ 0.00116457
    }
    optimized["System Cost"] = 361.99167985875346

    # Cálculo de la diferencia porcentual entre baseline y optimized para cada KPI,
    # renombrando las claves para PT según el ejemplo
    difference = {}
    for key in ["PT Frequency", "PT Delay", "Operational Cost", "Congestion (Delay)", "Emissions"]:
        base_val = baseline[key]
        opt_val = optimized[key]
        diff = (base_val - opt_val) / base_val if base_val != 0 else 0
        if key == "PT Frequency":
            diff_key = "PT Cost Freq"
        elif key == "PT Delay":
            diff_key = "PT Cost Delay"
        else:
            diff_key = key
        difference[diff_key] = diff

    # Para "System Cost" se define la diferencia en 0
    difference["System Cost"] = 0

    return {
        "baseline": baseline,
        "optimized": optimized,
        "difference": difference
    }

async def optimize_kpis(weights: dict) -> dict:
    """
    Selecciona la lógica de optimización en función del modo.
    En modo test se utiliza el cálculo simulado.
    """
    if settings.OPTIMIZATION_MODE == "test":
        time.sleep(1)  # Simula retraso en el procesamiento
        return await calculate_kpis(weights)
    else:
        return await optimize_kpis_real(weights)

async def optimize_kpis_real(weights: dict) -> dict:
    """
    Llama al servicio de optimización real mediante una solicitud HTTP.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.OPTIMIZATION_SERVICE_URL, json={"weights": weights})
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"error": f"Error en la consulta al servicio de optimización: {e}"}
