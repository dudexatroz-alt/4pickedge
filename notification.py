from dataclasses import dataclass

@dataclass
class Alert:
    title: str
    body: str
    kind: str
    dedupe_key: str

def pick_result_alert(selection_text, result, game):
    symbols={"W":"✅","L":"❌","P":"↔️"}
    labels={"W":"GANADA","L":"PERDIDA","P":"PUSH"}
    if result not in symbols:
        return None
    return Alert(
        title=f'{symbols[result]} {labels[result]}',
        body=f'{selection_text} · {game}',
        kind="pick_result",
        dedupe_key=f"result:{game}:{selection_text}:{result}",
    )

def edge_change_alert(selection_text, old_edge, new_edge):
    if old_edge is None or new_edge is None:
        return None
    change=float(new_edge)-float(old_edge)
    if abs(change)<.04:
        return None
    direction="subió" if change>0 else "bajó"
    return Alert(
        title="Cambio importante de edge",
        body=f'{selection_text}: {direction} {abs(change)*100:.1f} puntos',
        kind="edge_change",
        dedupe_key=f"edge:{selection_text}:{round(new_edge,3)}",
    )
