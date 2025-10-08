# core/calculations.py
import numpy as np
import pandas as pd

def calc_unit_economics(price, cost_acai, cost_fruits, cost_granola):
    """Calcula el margen bruto unitario."""
    variable_cost = cost_acai + cost_fruits + cost_granola
    gross_margin = price - variable_cost
    margin_pct = (gross_margin / price) * 100
    return {
        "Precio [Bs]": price,
        "Costo Variable [Bs]": variable_cost,
        "Margen Bruto [Bs]": gross_margin,
        "Margen [%]": margin_pct
    }

def calcular_van_tir(flujos, tasa):
    """
    Calcula VAN y TIR a partir de una lista de flujos de caja mensuales.
    VAN = Valor Actual Neto, TIR = Tasa Interna de Retorno.
    """
    flujos_np = np.array(flujos)
    meses = np.arange(len(flujos_np))
    van = np.sum(flujos_np / (1 + tasa) ** meses)
    try:
        tir = np.irr(flujos_np)
    except Exception:
        tir = np.nan
    return round(van, 2), round(tir if tir is not None else 0, 4)

def calcular_payback(flujos):
    """
    Calcula el mes en el que se recupera la inversión (Payback).
    Retorna el número de mes donde el flujo acumulado supera 0.
    """
    acumulado = np.cumsum(flujos)
    meses_recuperacion = np.argmax(acumulado >= 0)
    return int(meses_recuperacion + 1) if acumulado[-1] > 0 else None
