# 4 Pick Edge — Etapa 35 Final Beta Bundle

This is the deployable merge of the latest app architecture.

Included:
- MLB public schedule/final feed connectors
- verified Polymarket outcome/token mapping
- public midpoint pricing
- advanced intrinsic model bundle
- Top 4 eligibility/ranking
- SQLite snapshot/result history
- automatic MLB settlement
- alert objects
- Render Blueprint (`render.yaml`)
- Docker/Gunicorn deployment

## Important operational limitation
I cannot publish the service into your external Render/GitHub account from this chat because no authenticated hosting/account-control tool is connected here.

The package is now prepared for deployment. On Render, the Blueprint can create the web service and persistent disk. Render currently supports Flask with Gunicorn, health check paths, HTTPS/TLS, and persistent disks for paid web services.

## After the first public deploy
Run:
`APP_BASE_URL=https://YOUR-SERVICE.onrender.com python healthcheck.py`

Then verify a real game date and a completed game before treating live results as production-validated.
