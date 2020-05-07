from redis.client import Redis


def get_r():
    r = Redis(host='redis')
    return r

