# 4 Pick Edge — Etapa 40

- Picks manuales vinculados al `game_pk` real de MLB.
- Selector de Moneyline, Total, Run Line y NRFI/YRFI.
- Lado normalizado (`home`, `away`, `over`, `under`, `nrfi`, `yrfi`).
- Línea persistente para Total/Run Line con migración SQLite segura.
- `/api/settle` puede cerrar picks manuales vinculados cuando el juego sea Final.
- Health version: `4.0-settlement-ready`.
