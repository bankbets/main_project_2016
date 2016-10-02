import random, os
import uuid, hashlib

def roll(user, amt, c_seed):
    s_seed = uuid.uuid4().hex
    m_seed = c_seed + "_" + s_seed
    f_seed = hashlib.sha224(m_seed).hexdigest()
    res = 0
    for i in f_seed:
        res = res * 10
        res = res + ord(i)
    random.seed(res)
    result = random.randint(1, 100)
    return [result, s_seed, f_seed]