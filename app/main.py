from fastapi import FastAPI, HTTPException
import redis
import uuid

from config import settings

pool = redis.ConnectionPool(host=settings.redishost, port=settings.port, db=settings.db)
r = redis.Redis(connection_pool=pool)
app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.get("/get/{key}")
async def getkey(key: str):
    r.hincrby("stats", "requests", amount=1)
    name = "default" + key
    if r.exists(name) == 1:
        return {"value": r.hget(name, "value")}
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/get/{namespace}/{key}")
async def getkeyns(key: str, namespace: str):
    r.hincrby("stats", "requests", amount=1)
    name = namespace + key
    if r.exists(name) == 1:
        return {"value": r.hget(name, "value")}
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/set/{key}")
async def setkey(key: str, value: int):
    r.hincrby("stats", "requests", amount=1)
    name = "default" + key
    if r.exists(name) == 1:
        erval = int(r.hget(name, "enable_reset"))
        if erval == 0:
            raise HTTPException(status_code=403, detail="Cannot set new value for keys with enable_reset set to false")
        elif erval == 1:
            oldval = r.hget(name, "value")
            r.hset(name, key='value', value=value)
            r.hincrby("stats", "keys_updated", amount=1)
            return {"old_value": oldval, "value": r.hget(name, "value")}
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/set/{namespace}/{key}")
async def setkeyns(key: str, namespace: str, value: int):
    r.hincrby("stats", "requests", amount=1)
    name = namespace + key
    if r.exists(name) == 1:
        erval = int(r.hget(name, "enable_reset"))
        if erval == 0:
            raise HTTPException(status_code=403, detail="Cannot set new value for keys with enable_reset set to false")
        elif erval == 1:
            oldval = r.hget(name, "value")
            r.hset(name, key='value', value=value)
            r.hincrby("stats", "keys_updated", amount=1)
            return {"old_value": oldval, "value": r.hget(name, "value")}
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/update/{key}")
async def updatekey(key: str, value: int):
    r.hincrby("stats", "requests", amount=1)
    name = "default" + key
    if r.exists(name) == 1:
        upper = int(r.hget(name, "update_upperbound"))
        lower = int(r.hget(name, "update_lowerbound"))
        if (value > upper or value < lower):
            raise HTTPException(status_code=403, detail="Value exceeds bounds set for key")
        else:
            r.hincrby(name, "value", amount=value)
            r.hincrby("stats", "keys_updated", amount=1)
            return {"value": r.hget(name, "value")}
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/update/{namespace}/{key}")
async def updatekeyns(key: str, namespace: str, value: int):
    r.hincrby("stats", "requests", amount=1)
    name = namespace + key
    if r.exists(name) == 1:
        upper = int(r.hget(name, "update_upperbound"))
        lower = int(r.hget(name, "update_lowerbound"))
        if (value > upper or value < lower):
            raise HTTPException(status_code=403, detail="Value exceeds bounds set for key")
        else:
            r.hincrby(name, "value", amount=value)
            r.hincrby("stats", "keys_updated", amount=1)
            return {"value": r.hget(name, "value")}
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/hit/{key}")
async def hitkey(key: str):
    name = "default" + key
    if r.exists(name) == 1:
        r.hincrby(name, "value", amount=1)
        r.hincrby("stats", "requests", amount=1)
        r.hincrby("stats", "keys_updated", amount=1)
        return {"value": r.hget(name, "value")}
        pass
    elif r.exists(name) == 0:
        await create(key, "default")
        await hitkey(key)
        return {"value": r.hget(name, "value")}
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/hit/{namespace}/{key}")
async def hitkeyns(key: str, namespace: str):
    name = namespace + key
    if r.exists(name) == 1:
        r.hincrby(name, "value", amount=1)
        r.hincrby("stats", "requests", amount=1)
        r.hincrby("stats", "keys_updated", amount=1)
        return {"value": r.hget(name, "value")}
    elif r.exists(name) == 0:
        await create(key, namespace)
        await hitkeyns(key, namespace)
        return {"value": r.hget(name, "value")}
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/create")
async def create(key: str = "", namespace: str = "default", value: int = 0, enable_reset: int = 0, update_lowerbound: int = -1, update_upperbound: int = 1):
    r.hincrby("stats", "requests", amount=1)
    if key == "":
        key = str(uuid.uuid4())
    name = namespace + key
    if r.exists(name) == 1:
        raise HTTPException(status_code=400, detail="Namespace and key " + namespace + ": " + key + " already exist")
    elif r.exists(name) == 0:
        if namespace == "stats":
            raise HTTPException(status_code=403, detail="Reserved keyword stats cannot be used for namespace")
        dict = {"key": key,
                "value": value,
                "namespace": namespace,
                "enable_reset": enable_reset,
                "update_lowerbound": update_lowerbound,
                "update_upperbound": update_upperbound}
        r.hset(name, key="value", value=value, mapping=dict)
        r.hincrby("stats", "keys_created", amount=1)
        #r.hset(namespace + key, key=key, value = value)
        return {"namespace": namespace, "key": r.hget(name, 'key'), "value": r.hget(name, 'value')}
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
@app.get("/info/{key}")
async def infokeyonly(key: str):
    r.hincrby("stats", "requests", amount=1)
    name = "default" + key
    if r.exists(name) == 1:
        return r.hgetall(name)
    elif r.exists(name) == 0:
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/info/{namespace}/{key}")
async def info(key: str, namespace: str):
    r.hincrby("stats", "requests", amount=1)
    name = namespace + key
    if r.exists(name) == 1:
        return r.hgetall(name)
    elif r.exists(name):
        raise HTTPException(status_code=400, detail="Namespace and key do not exist")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/stats")
async def stats():
    r.hincrby("stats", "requests", amount=1)
    return r.hgetall("stats")

@app.on_event("startup")
async def createstats():
    if r.exists("stats"):
        pass
    else:
        statsdict = {"keys_created": 0,
                "keys_updated": 0,
                "requests": 0,
                "version": 1.0}
        r.hmset("stats", statsdict)