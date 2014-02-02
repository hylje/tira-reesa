"""Provide a human-compatible and testable interface to reesa.c using
ctypes
"""

import ctypes
import json

# Set up the underlying C library

reesa_so = ctypes.CDLL("_reesa.so")
reesa_so.readpriv.argtypes = [ctypes.c_char_p]*6
reesa_so.readpriv.restype = ctypes.c_void_p
reesa_so.genpriv.restype = ctypes.c_void_p
reesa_so.writepriv.argtypes = [ctypes.c_void_p]
reesa_so.writepriv.restype = ctypes.c_long

MAX_NUMBER_SIZE = ctypes.c_int.in_dll(reesa_so, "MAX_NUMBER_SIZE").value

def gen_key(filename):
    """Generate a key and save it to file

    Not tested since the generation function is not implemented yet.
    """
    pk = reesa_so.genpriv()
    
    p, q, privexp, pubexp, modulus, totient_modulus = [
        ctypes.create_string_buffer("", MAX_NUMBER_SIZE) 
        for i in range(6) 
    ]

    reesa_so.writepriv(pk, p, q, privexp, pubexp, modulus, totient_modulus)

    try:
        f = open(filename, "w")
        json.dump(f, {"p": p.value, 
                      "q": q.value, 
                      "private_exponent": private_exponent.value, 
                      "public_exponent": public_exponent.value, 
                      "modulus": modulus.value, 
                      "totient_modulus": totient_modulus.value})
    finally:
        f.close()


class InvalidPrivkey(Exception):
    pass

class NotJSONPrivkey(InvalidPrivkey):
    pass

class IncompletePrivkey(InvalidPrivkey):
    pass

class UnacceptablePrivkey(InvalidPrivkey):
    pass

def load_key(filename): 
    """Load the key as priv/pubkey depending on its content, validate it
    and and show information about it

    """
    try:
        f = open(filename)
        pk_dat = json.load(f)
    except ValueError:
        raise NotJSONPrivkey("That private key is not valid JSON")
    finally:
        f.close()
    
    try:
        pk = reesa_so.readpriv(pk_dat["p"],
                               pk_dat["q"],
                               pk_dat["private_exponent"],
                               pk_dat["public_exponent"],
                               pk_dat["modulus"],
                               pk_dat["totient_modulus"])
    except KeyError:
        raise IncompletePrivkey("That private key is missing required values.")

    if pk is None:
        raise UnacceptablePrivkey("That private key has invalid values.")

    p, q, privexp, pubexp, modulus, totient_modulus = [
        ctypes.create_string_buffer("", MAX_NUMBER_SIZE) for i in range(6)
    ]

    reesa_so.writepriv(pk, p, q, privexp, pubexp, modulus, totient_modulus)

    return {
        "p": p.value,
        "q": q.value,
        "private_exponent": privexp.value,
        "public_exponent": pubexp.value,
        "modulus": modulus.value,
        "totient_modulus": totient_modulus.value
    }

def encrypt(pubkey, plaintext):
    "Encrypt plaintext using the public/private key given"
    
def decrypt(privkey, ciphertext):
    "Decrypt ciphertext using the private key given"
