import time

import redis


print('waiting for redis')
time.sleep(5)

r = redis.StrictRedis(host='redis', port=6379, db=0)

print('starting bot')
while True:
    turn = r.blpop('turn')
    print('turn', turn)

