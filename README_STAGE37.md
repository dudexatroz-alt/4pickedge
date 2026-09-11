# 4 Pick Edge — Etapa 37 Push Ready

Se añadió:
- PWA manifest.
- Service Worker con recepción/click de push.
- Registro de suscripciones en SQLite.
- Endpoints `/api/push/public-key`, `/api/push/subscribe` y `/api/push/test`.
- Envío con Web Push/VAPID mediante `pywebpush`.
- Variables de entorno para VAPID.

No se incluyen claves VAPID reales. Deben configurarse únicamente en el servidor HTTPS.
No hay trading ni órdenes automáticas.

## Para activar push real
1. Desplegar el servicio por HTTPS.
2. Generar un par VAPID.
3. Configurar `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_CLAIM_EMAIL`.
4. Abrir la app y pulsar “Activar notificaciones”.
5. Ejecutar `/api/push/test` desde el backend o conectar el emisor a eventos de resultado/edge.
