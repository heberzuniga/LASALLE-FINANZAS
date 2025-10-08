# core/assumptions.py
# Define los valores base del modelo (redondeados del Excel original)

def get_default_assumptions():
    """Devuelve los valores base iniciales para el modelo financiero."""
    return {
        # Precios por bowl
        "price_talla_m": 30.0,
        "price_talla_s": 28.0,

        # Costos variables
        "cost_acai_m": 12.7,
        "cost_acai_s": 8.7,
        "cost_fruits": 3.0,
        "cost_granola": 1.2,

        # Días laborales y producción
        "units_per_day": 40,
        "working_days": 26,

        # Costos fijos
        "fixed_costs": 3000.0,

        # Tasa de descuento (editable)
        "discount_rate": 0.10
    }
