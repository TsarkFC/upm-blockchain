import base64, hashlib, random
from datetime import datetime
import time
import pandas as pd

data_storage = {}

def hash_cash(n_zeros, resource):
    st = time.time()
    df = pd.read_csv("final_results.csv",  index_col=[0])

    ver = '1'
    date = create_date()
    nonce_counter = 0
    rand = generate_random()
    nonce = create_nonce(0)
    
    header = ":".join([ver, n_zeros, date, resource, '', rand, nonce])
    hash_string = compute_hash(header)
    
    while not verify_leading_zeros(n_zeros, hash_string):
        nonce_counter += 1
        nonce = create_nonce(nonce_counter)
        header = ":".join([ver, n_zeros, date, resource, '', rand, nonce])
        hash_string = compute_hash(header)
        
    et = time.time()
    tt = et - st
    new= {'numb_zeros' : n_zeros, 'time' : tt, 'n_trials' : nonce_counter}
    df = df.append(new, ignore_index=True)
    df.to_csv("final_results.csv")
    print(tt)
    print(nonce_counter)
    print(hash_string)
    return ""

def verify_leading_zeros(n_zeros, hash_string):
    for i in range(int(n_zeros)):
        if hash_string[i] != '0': return False
    return True

def to_binary(s):
    return bin(int(s, 16))

def compute_hash(s):
    hash_object = hashlib.sha1(s.encode())
    hash_hex = hash_object.hexdigest()
    hash_size = len(hash_hex) * 4
    hash_bin = (bin(int(hash_hex, 16))[2:]).zfill(hash_size)
    return hash_bin

def create_date():
    return datetime.now().strftime('%y%m%d%H%M')
    
def create_nonce(n):
    n = str(n)
    n_string_bytes = n.encode("ascii")
    base64_string_bytes = base64.b64encode(n_string_bytes)
    n_coded= base64_string_bytes.decode("ascii")
    return n_coded

def generate_random(random_chars=16, alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=/"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])

if __name__ == '__main__':
    hash_cash('50', 'test@gmail.com')
