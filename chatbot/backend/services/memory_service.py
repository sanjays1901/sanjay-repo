import json
from redis_client import redis_client

def build_session_key( tenant_id, session_id):
    return f"{tenant_id}:{session_id}"

def get_history(tenant_id, session_id):
    if not session_id:
        return []
    
    session_key = build_session_key(tenant_id, session_id)

    # Geting data from Redis
    history_json = redis_client.get(session_key)
    if not history_json:
        return []
    history = json.loads(history_json)

    return history[-6:]


def save_history(tenant_id, session_id, query, answer):

    if not session_id:
        return
    
    session_key = build_session_key(tenant_id, session_id)

    history_json = redis_client.get(session_key)
    if history_json:
        history = json.loads(history_json)
    else:
        history = []

    history += [{"role": "user", "content": query}, {"role": "assistant", "content": answer}]
    # Saving data to Redis
    redis_client.setex(session_key, 3600, json.dumps(history))