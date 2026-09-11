def elite_gate(*, model_validated, model_prob, edge, data_quality,
               historical_n, historical_hit_rate, calibrated=True):
    reasons=[]
    if not model_validated: reasons.append("modelo_no_validado")
    if not calibrated: reasons.append("probabilidad_no_calibrada")
    if model_prob < .85: reasons.append("probabilidad_menor_85")
    if edge is None or edge < .04: reasons.append("edge_menor_4pp")
    if data_quality < 80: reasons.append("calidad_datos_menor_80")
    if historical_n < 40: reasons.append("muestra_historica_menor_40")
    if historical_hit_rate is None or historical_hit_rate < .60:
        reasons.append("hit_rate_historico_menor_60")
    return {"approved":not reasons,"reasons":reasons}

def selection_label(gate, has_pick=True):
    if not has_pick:return "SIN PICK #1"
    return "SEÑAL ÉLITE VALIDADA" if gate["approved"] else "MEJOR DISPONIBLE · NO ÉLITE"
