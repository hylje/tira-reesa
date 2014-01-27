#include <gmp.h>
#include <stdlib.h>
#include <stdbool.h>

/* Pregenerated series of small primes
static mpz_t[] first_primes;
 */


/* The internal private key format uses GMP big integers. */
struct reesa_privkey {
  mpz_t p;
  mpz_t q;
  mpz_t public_exponent;
  mpz_t private_exponent;
  mpz_t modulus;
  mpz_t totient_modulus;
} reesa_priv;

/* The internal public key format is a subset of the private key's
   fields. 
*/
struct reesa_pubkey {
  mpz_t public_exponent;
  mpz_t modulus;
} reesa_pub;

struct reesa_privkey* genpriv () {
  /* Allocate a new private key ready-to-use */
  struct reesa_privkey* priv = malloc(sizeof(struct reesa_privkey));
  
  /* WIP */

  return priv;
}

struct reesa_privkey* readpriv(
	     char* p, 
	     char* q, 
	     char* public_exponent, 
	     char* private_exponent, 
	     char* modulus, 
	     char* totient_modulus) {
  /* Read the given integers (as strings) into the internal GMP data
     structure.

     The caller is responsible for deallocating the strings we are
     given.

     If any of the given strings are invalid (not base 10 integers),
     returns NULL deallocating the struct.
  */

  struct reesa_privkey* priv = malloc(sizeof(struct reesa_privkey));
  _Bool fail = false;

  mpz_init(priv->p);
  fail |= mpz_set_str(priv->p, p, 10) == -1;
  
  mpz_init(priv->q);
  fail |= mpz_set_str(priv->q, q, 10) == -1;

  mpz_init(priv->public_exponent);
  fail |= mpz_set_str(priv->public_exponent, public_exponent, 10) == -1;

  mpz_init(priv->private_exponent);
  fail |= mpz_set_str(priv->private_exponent, private_exponent, 10) == -1;

  mpz_init(priv->modulus);
  fail |= mpz_set_str(priv->modulus, modulus, 10) == -1;

  mpz_init(priv->totient_modulus);
  fail |= mpz_set_str(priv->totient_modulus, totient_modulus, 10) == -1;

  if (fail) {
    free(priv);
    return NULL;
  }

  return priv;
}

int writepriv(struct reesa_privkey* priv, 
	      int (*callback)(char*, char*, char*, char*, char*, char*)) {
  /* Write back our internal data structure for the given callback. 

     The callback is responsible for deallocating the strings we give
     it.
   */
 
  int retval = (*callback)(
     mpz_get_str(NULL, 10, priv->p),
     mpz_get_str(NULL, 10, priv->q),
     mpz_get_str(NULL, 10, priv->public_exponent),
     mpz_get_str(NULL, 10, priv->private_exponent),
     mpz_get_str(NULL, 10, priv->modulus),
     mpz_get_str(NULL, 10, priv->totient_modulus)
  );

  return retval;
}

struct reesa_pubkey* priv2pub (struct reesa_privkey* priv) {
  /* Strip privates, returning just the public key */
  struct reesa_pubkey* pub = malloc(sizeof(struct reesa_pubkey));
  
  mpz_init(pub->public_exponent);
  mpz_set(pub->public_exponent, priv->public_exponent);
  mpz_init(pub->modulus);
  mpz_set(pub->modulus, priv->modulus);
  
  return pub;
}

/* TODO consider using python to do the serialization and just
   initialize old keys from a set of arguments using ctypes */

int readpub() { 
  /* WIP */ 
  return 99;
}
int writepub() { 
  /* WIP */ 
  return 99;
}

void encrypt(struct reesa_pubkey* pub, 
	     const char* plaintext, 
	     int plaintext_length, 
	     char* ciphertext) {
  /* WIP */
}

void decrypt(struct reesa_privkey* priv,
	     const char* ciphertext,
	     int ciphertext_length,
	     char* plaintext) {
  /* WIP */
}

void sign(struct reesa_privkey* priv, 
	  const char* text,
	  int text_length,
	  char* signature) {
  /* WIP (maybe) */
}

void verify(struct reesa_privkey* pub,
	    const char* text,
	    int text_length,
	    char* signature) {
  /* WIP (maybe) */
}
