import os, json

def push_enabled():
    return bool(os.getenv("VAPID_PRIVATE_KEY") and os.getenv("VAPID_PUBLIC_KEY") and os.getenv("VAPID_CLAIM_EMAIL"))

def send_push(subscription, *, title, body, url="/"):
    if not push_enabled():
        return {"sent":False,"reason":"push_not_configured"}
    try:
        from pywebpush import webpush
        webpush(
            subscription_info=subscription,
            data=json.dumps({"title":title,"body":body,"url":url}),
            vapid_private_key=os.environ["VAPID_PRIVATE_KEY"],
            vapid_claims={"sub":f'mailto:{os.environ["VAPID_CLAIM_EMAIL"]}'}
        )
        return {"sent":True}
    except Exception as e:
        return {"sent":False,"reason":str(e)}
