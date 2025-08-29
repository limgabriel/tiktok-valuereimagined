# simple in-memory cache for POC
_CACHE = {}

def put(video_id, payload):
    _CACHE[video_id] = payload

def get(video_id):
    return _CACHE.get(video_id)
