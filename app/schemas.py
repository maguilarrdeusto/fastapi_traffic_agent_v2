from pydantic import BaseModel
from typing import Dict

class OptimizationInput(BaseModel):
    data: Dict[str, float]  # Los valores a optimizar (weights)

class KPIResults(BaseModel):
    baseline: Dict[str, float]
    optimized: Dict[str, float]
    difference: Dict[str, float]

class OptimizationOutput(BaseModel):
    KPIs: KPIResults
