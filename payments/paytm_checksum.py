# payments/paytm_checksum.py
# Source: Paytm official checksum library (updated for pycryptodome)

import base64
import string
import random
import hashlib
from Crypto.Cipher import AES

IV = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16


def generate_checksum(param_dict, merchant_key, salt=None):
    params_string = __get_params_string(param_dict)
    salt = salt or __id_generator(4)
    final_string = f"{params_string}|{salt}"

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string = f"{hash_string}|{salt}"

    return __encode(hash_string, IV, merchant_key)


def verify_checksum(param_dict, merchant_key, checksum):
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')

    params_string = __get_params_string(param_dict)
    try:
        salt = __decode(checksum, IV, merchant_key).split('|')[-1]
    except Exception:
        return False

    regenerated_checksum = generate_checksum(param_dict, merchant_key, salt=salt)
    return regenerated_checksum == checksum


def generate_checksum_by_str(params_string, merchant_key, salt=None):
    salt = salt or __id_generator(4)
    final_string = f"{params_string}|{salt}"

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string = f"{hash_string}|{salt}"

    return __encode(hash_string, IV, merchant_key)


def verify_checksum_by_str(params_string, merchant_key, checksum):
    try:
        salt = __decode(checksum, IV, merchant_key).split('|')[-1]
    except Exception:
        return False
    regenerated = generate_checksum_by_str(params_string, merchant_key, salt=salt)
    return regenerated == checksum


def __id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def __get_params_string(param_dict):
    params_string_list = []
    for key in sorted(param_dict.keys()):
        value = param_dict[key]
        params_string_list.append('' if value == 'null' else str(value))
    return '|'.join(params_string_list)


def __pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def __unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def __encode(to_encode, iv, key):
    key = hashlib.sha256(key.encode()).digest()[:BLOCK_SIZE * 2]  # 32 bytes
    padded = __pad(to_encode).encode()
    c = AES.new(key, AES.MODE_CBC, iv.encode())
    encoded = base64.b64encode(c.encrypt(padded))
    return encoded.decode("UTF-8")


def __decode(to_decode, iv, key):
    key = hashlib.sha256(key.encode()).digest()[:BLOCK_SIZE * 2]
    c = AES.new(key, AES.MODE_CBC, iv.encode())
    decoded = c.decrypt(base64.b64decode(to_decode))
    return __unpad(decoded).decode("UTF-8")