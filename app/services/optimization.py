import time
import httpx
from app.config import settings

async def calculate_kpis(weights: dict) -> dict:
    # Normalizar los pesos si la suma es mayor a 1
    total_weight = sum(weights.values())
    if total_weight > 1:
        weights = {k: v / total_weight for k, v in weights.items()}
    
    # Extraemos los pesos para mayor legibilidad
    w_pt = weights["weight_PublicTransport"]
    w_oc = weights["weight_OperationalCost"]
    w_cong = weights["weight_Congestion"]
    w_em = weights["weight_Emissions"]

    # Fórmulas que combinan términos lineales y cuadráticos para simular efectos no lineales
    baseline = {
        "PT Frequency": w_pt * 50 + (w_pt ** 2) * 10,
        "PT Delay": w_pt * 400 + (w_pt ** 2) * 50,
        "Operational Cost": w_oc * 0.3 + (w_oc ** 2) * 0.1,
        "Congestion (Delay)": w_cong * 0.8 + (w_cong ** 2) * 0.1,
        "Emissions": w_em * 0.007 + (w_em ** 2) * 0.001,
    }
    baseline["System Cost"] = 468.38604563398485

    optimized = {
        "PT Frequency": w_pt * 45 + (w_pt ** 2) * 8,
        "PT Delay": w_pt * 360 + (w_pt ** 2) * 40,
        "Operational Cost": w_oc * 0.4 + (w_oc ** 2) * 0.12,
        "Congestion (Delay)": w_cong * 1.0 + (w_cong ** 2) * 0.15,
        "Emissions": w_em * 0.007 + (w_em ** 2) * 0.0008,
    }
    optimized["System Cost"] = 361.99167985875346

    # Cálculo de la diferencia porcentual
    difference = {}
    for key in ["PT Frequency", "PT Delay", "Operational Cost", "Congestion (Delay)", "Emissions"]:
        base_val = baseline[key]
        opt_val = optimized[key]
        diff = (base_val - opt_val) / base_val if base_val != 0 else 0
        # Renombrar claves para PT según el ejemplo
        if key == "PT Frequency":
            diff_key = "PT Cost Freq"
        elif key == "PT Delay":
            diff_key = "PT Cost Delay"
        else:
            diff_key = key
        difference[diff_key] = diff

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
