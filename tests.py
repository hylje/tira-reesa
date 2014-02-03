"""WIP: Test the implemented functionality using Unittest"""

import unittest
import tempfile
import json
import ctypes
from decimal import Decimal, localcontext

import reesa

class TestCLibrary(unittest.TestCase):
    def test_roundtrip(self):
        privkey_values = ("123", "234", "345", "456", "567", "678")

        privkey = reesa.reesa_so.readpriv(*privkey_values)

        p, q, privexp, pubexp, modulus, totient_modulus = [
            ctypes.create_string_buffer("", reesa.MAX_NUMBER_SIZE) for i in range(6)
        ]

        retval = reesa.reesa_so.writepriv(privkey, p, q, privexp, pubexp, modulus, totient_modulus)

        self.assertEqual(retval, 1)

        self.assertEqual(p.value, "123")
        self.assertEqual(q.value, "234")
        self.assertEqual(privexp.value, "345")
        self.assertEqual(pubexp.value, "456")
        self.assertEqual(modulus.value, "567")
        self.assertEqual(totient_modulus.value, "678")

    def test_generator(self):
        privkey = reesa.reesa_so.genpriv()

        p, q, privexp, pubexp, modulus, totient_modulus = [
            ctypes.create_string_buffer("", reesa.MAX_NUMBER_SIZE) for i in range(6)
        ]

        retval = reesa.reesa_so.writepriv(privkey, p, q, pubexp, privexp, modulus, totient_modulus)

        q = Decimal(q.value)
        p = Decimal(p.value)

        self.assertEqual(retval, 1)
        
        with localcontext() as ctx:
            # use higher precision to match gmp
            ctx.prec = 200
            self.assertEqual(Decimal(modulus.value),
                             p*q)
            
            self.assertEqual(Decimal(totient_modulus.value), 
                             (p-1)*(q-1))
            
            self.assertEqual(pubexp.value, "65537")
            
            self.assertEqual(
                Decimal(privexp.value), 
                inverse(Decimal(pubexp.value), 
                        Decimal(totient_modulus.value)))

    def test_generator_randomness(self):
        priv1 = reesa.reesa_so.genpriv()
        priv2 = reesa.reesa_so.genpriv()
        
        dat1 = reesa.dump_privkey(priv1)
        dat2 = reesa.dump_privkey(priv2)
        
        for key in ["p", "q"]:
            self.assertNotEqual(dat1[key], dat2[key], msg="Key: %s, %s == %s" % (key, dat1[key], dat2[key]))
                                 
def inverse(a, n): 
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return None
    if t < 0:
        t += n
    return t
            
class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.valid_fp = tempfile.NamedTemporaryFile()
        self.valid_filename = self.valid_fp.name
        self.valid_test_data = {
            "p": "123",
            "q": "234",
            "private_exponent": "345",
            "public_exponent": "456",
            "modulus": "567",
            "totient_modulus": "678"
        }
        json.dump(self.valid_test_data, self.valid_fp)
        self.valid_fp.flush()

        self.incomplete_fp = tempfile.NamedTemporaryFile()
        self.incomplete_filename = self.incomplete_fp.name
        self.incomplete_test_data = {
            "p": "123"
        }
        json.dump(self.incomplete_test_data, self.incomplete_fp)
        self.incomplete_fp.flush()

        self.invalid_fp = tempfile.NamedTemporaryFile()
        self.invalid_filename = self.invalid_fp.name
        self.invalid_test_data = {
            "p": "not a number",
            "q": "123",
            "private_exponent": "123",
            "public_exponent": "123",
            "modulus": "123",
            "totient_modulus": "123"
        }
        json.dump(self.invalid_test_data, self.invalid_fp)
        self.invalid_fp.flush()

        self.invalid_json_fp = tempfile.NamedTemporaryFile()
        self.invalid_json_filename = self.invalid_json_fp.name
        self.invalid_json_test_data = "a"
        self.invalid_json_fp.write(self.invalid_json_test_data)
        self.invalid_json_fp.flush()

    def testLoad(self):
        retval = reesa.load_key(self.valid_filename)
        self.assertEqual(retval, self.valid_test_data)

    def testIncompleteLoad(self):
        def closure():
            reesa.load_key(self.incomplete_filename)
    
        self.assertRaises(reesa.IncompletePrivkey, closure)

    def testInvalidLoad(self):
        def closure():
            reesa.load_key(self.invalid_filename)
        
        self.assertRaises(reesa.UnacceptablePrivkey, closure)

    def testInvalidJSON(self):
        def closure():
            reesa.load_key(self.invalid_json_filename)
        
        self.assertRaises(reesa.NotJSONPrivkey, closure)
