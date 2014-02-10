"""Tool that provides reasonably convenient access to the reesa C
library for generating keypairs, encryption and decryption using a RSA
scheme.
"""

import ctypes
import json

# Set up the underlying C library

reesa_so = ctypes.CDLL("_reesa.so")
reesa_so.readpriv.argtypes = [ctypes.c_char_p]*6
reesa_so.readpriv.restype = ctypes.c_void_p
reesa_so.genpriv.restype = ctypes.c_void_p
reesa_so.writepriv.argtypes = [ctypes.c_void_p] + [ctypes.c_char_p]*6
reesa_so.writepriv.restype = ctypes.c_long
reesa_so.encrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long]
reesa_so.encrypt.restype = ctypes.c_long
reesa_so.decrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long]
reesa_so.decrypt.restype = ctypes.c_long


MAX_NUMBER_SIZE = ctypes.c_int.in_dll(reesa_so, "MAX_NUMBER_SIZE").value

def gen_key(filename):
    """Generate a key and save it to file
    """
    pk = reesa_so.genpriv()
            
    try:
        f = open(filename, "w")
        json.dump(dump_privkey(pk), f)
    finally:
        f.close()

def dump_privkey(privkey):
    p, q, public_exponent, private_exponent, modulus, totient_modulus = [
        ctypes.create_string_buffer("", MAX_NUMBER_SIZE) 
        for i in range(6) 
    ]
    
    reesa_so.writepriv(privkey, p, q, public_exponent, private_exponent, modulus, totient_modulus)

    return {"p": p.value, 
            "q": q.value, 
            "private_exponent": private_exponent.value, 
            "public_exponent": public_exponent.value, 
            "modulus": modulus.value, 
            "totient_modulus": totient_modulus.value}

class InvalidPrivkey(Exception):
    pass

class NotJSONPrivkey(InvalidPrivkey):
    pass

class IncompletePrivkey(InvalidPrivkey):
    pass

class UnacceptablePrivkey(InvalidPrivkey):
    pass

def get_key(filename):
    """Loads a priv/pubkey and returns a pointer to it for use in the C
    library

    May raise a InvalidPrivkey exception subclass if the key could not
    be loaded.
    """

    try:
        f = open(filename)
        key_dat = json.load(f)
    except ValueError:
        raise NotJSONPrivkey("That private key is not valid JSON")
    finally:
        f.close()
    
    # TODO: separate loading procedure for pubkeys

    try:
        priv = pub = reesa_so.readpriv(
            key_dat["p"],
            key_dat["q"],
            key_dat["public_exponent"],
            key_dat["private_exponent"],
            key_dat["modulus"],
            key_dat["totient_modulus"])
    except KeyError:
        raise IncompletePrivkey("That private key is missing required values.")

    if priv is None:
        raise UnacceptablePrivkey("That private key has invalid values.")

    return priv, pub

def load_key(filename): 
    """Load the key as priv/pubkey depending on its content, validate it
    and and show information about it

    """
    privkey, pubkey = get_key(filename)

    if privkey is not None:
        return dump_privkey(privkey)
    if pubkey is not None:
        # TODO
        return dump_pubkey(pubkey)

def blockify(source, chunk_size):
    """Splits a file stream into standard-sized blocks, padding if
    necessary
    """
    chunk = source.read(chunk_size)
    while chunk:
        if len(chunk) < chunk_size:
            chunk += "\x00" * (chunk_size - len(chunk))
        yield chunk
        chunk = source.read(chunk_size)

def pad(chunk):
    pass

def unpad(chunk):
    pass

class BlockError(Exception):
    "Something went wrong with the block processing"

CHUNK_SIZE_PLAIN = 16
CHUNK_SIZE_CIPHER = 32

def block_process(function, key, source, target, chunk_read, chunk_write):
    """Processes the `source` filename with `function` blockwise and writes the
    result into `target` filename.
    """ 

    chunk_read_hex = chunk_read*2+1
    chunk_write_hex = chunk_write*2+1

    inbuf = ctypes.create_string_buffer("", chunk_read_hex)
    outbuf = ctypes.create_string_buffer("", chunk_write_hex)

    try:
        # XXX doesn't check if files exist
        target_f = open(target, "wb")
        source_f = open(source, "rb")

        for block in blockify(source_f, chunk_read):
            inbuf.value = block.encode("hex")
            retval = function(key, inbuf, outbuf, chunk_write)
            if retval != 0:
                raise BlockError(retval)
            output_length = len(outbuf.value)
            if output_length < chunk_write*2:
                # deal with leading zeroes
                buf = "0"*(chunk_write*2-output_length) + outbuf.value
            elif output_length > chunk_write*2:
                # not enough leeway
                print outbuf.value
                print output_length, chunk_write*2
                raise BlockError("Too small write blocksize!")
            else:
                buf = outbuf.value

            target_f.write(buf.decode("hex").rstrip("\x00"))
    finally:
        target_f.close()
        source_f.close()

    return 1

def encrypt(pubkey, plaintext, ciphertext):
    "Encrypt plaintext using the public/private key given"
    priv, pub = get_key(pubkey)

    return block_process(
        reesa_so.encrypt, pub, plaintext, ciphertext,
        chunk_read=CHUNK_SIZE_PLAIN,
        chunk_write=CHUNK_SIZE_CIPHER
    )


class PrivkeyNeeded(Exception):
    pass

def decrypt(privkey, ciphertext, plaintext):
    "Decrypt ciphertext using the private key given"
    priv, pub = get_key(privkey)
    
    if not priv:
        raise PrivkeyNeeded("That key cannot be used to decrypt")

    return block_process(
        reesa_so.decrypt, priv, ciphertext, plaintext,
        chunk_read=CHUNK_SIZE_CIPHER,
        chunk_write=CHUNK_SIZE_PLAIN,
    )

ACTIONS = {
    "gen_key": gen_key,
    "show_key": load_key,
    "encrypt": encrypt,
    "decrypt": decrypt
}

def main(_, action, *args):
    if action == "help" and not args:
        print __doc__
        print
        print "Available commands:"
        for action in ACTIONS:
            print action
        print
        print "Try: %s help [command]" % _
    if action == "help" and len(args) == 1 and args[1] in ACTIONS:
        print ACTIONS[action].__doc__
    elif action in ACTIONS:
        print ACTIONS[action](*args)
    else:
        print "Not a valid action. Try: %s help" % _

if __name__ == "__main__":
    import sys
    main(*sys.argv)
