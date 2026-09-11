# 4 Pick Edge — Etapa 38 Dashboard

Cambios principales:
- La ruta `/` ahora muestra un dashboard funcional, no solo "Push Ready".
- Calendario MLB por fecha desde `/api/schedule`.
- Top 4 desde `/api/top4`, sin forzar picks si no superan filtros.
- Entrada manual opcional mediante `POST /api/top4/manual`.
- Historial/estadísticas y cierre automático de resultados.
- Badges ✅ GANÓ / ❌ PERDIÓ / ➖ PUSH / ⏳ PENDIENTE.
- Push/PWA conservado.
- Se eliminó la referencia a `/icon-192.png` que podía generar 404.
- Persistencia usa `APP_DB`, compatible con el disco de Render.
