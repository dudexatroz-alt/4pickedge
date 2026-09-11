import tempfile,os
from push_store import PushStore
from push_sender import push_enabled,send_push

fd,path=tempfile.mkstemp(suffix=".db");os.close(fd);os.unlink(path)
s=PushStore(path)
sub={"endpoint":"https://push.example/abc","keys":{"p256dh":"x","auth":"y"}}
s.upsert(sub)
rows=s.all()
assert len(rows)==1 and rows[0]["endpoint"]==sub["endpoint"]
assert push_enabled() is False
r=send_push(sub,title="T",body="B")
assert r["sent"] is False and r["reason"]=="push_not_configured"
s.remove_endpoint(sub["endpoint"])
assert s.all()==[]
os.remove(path)
print("push notification readiness tests OK")
