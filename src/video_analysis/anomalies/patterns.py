"""Cambios relativos a un tramo de referencia; no diagnóstico de daños."""

import numpy as np
from sklearn.ensemble import IsolationForest


def detect_patterns(windows, baseline_end, enabled=True):
    if not enabled:
        return {"status": "disabled", "events": [], "windows": []}
    baseline = [w for w in windows if w["end_seconds"] <= baseline_end]
    evaluation = [w for w in windows if w["start_seconds"] >= baseline_end]
    if len(baseline) < 8 or not evaluation:
        return {
            "status": "insufficient_reference",
            "events": [],
            "windows": [],
            "message": "Se requieren al menos 8 ventanas de referencia y una posterior; aumenta la duración de referencia o del video.",
        }
    features = ["original_rms", "original_p95"]
    x = np.array([[w[k] for k in features] for w in baseline])
    y = np.array([[w[k] for k in features] for w in evaluation])
    center = np.median(x, axis=0)
    # Piso absoluto evita alarmas por diferencias numéricas en escenas estáticas.
    scale = np.maximum(1.4826 * np.median(np.abs(x - center), axis=0), 0.02)
    train, query = (x - center) / scale, (y - center) / scale
    model = IsolationForest(n_estimators=100, contamination="auto", random_state=42, n_jobs=1)
    model.fit(train)
    decisions = model.decision_function(query)
    scores = np.max(np.abs(query), axis=1)
    records, events = [], []
    for window, score, decision in zip(evaluation, scores, decisions):
        # El criterio robusto explicable define la alerta. IF es evidencia auxiliar:
        # en una referencia constante un bosque no puede extrapolar confiablemente.
        record = {
            **window,
            "robust_score": float(score),
            "isolation_forest_decision": float(decision),
            "flagged": bool(score > 6),
        }
        records.append(record)
        if record["flagged"]:
            events.append(
                {
                    "start_seconds": window["start_seconds"],
                    "end_seconds": window["end_seconds"],
                    "score": float(score),
                }
            )
    return {
        "status": "evaluated",
        "reference_windows": len(baseline),
        "reference_end_seconds": baseline_end,
        "reference_assumption": "El tramo inicial seleccionado representa el comportamiento de referencia; requiere confirmación del usuario.",
        "features": features,
        "median": center.tolist(),
        "scale": scale.tolist(),
        "threshold": 6,
        "method": "MAD robusta; Isolation Forest como indicador auxiliar",
        "events": events,
        "windows": records,
    }
