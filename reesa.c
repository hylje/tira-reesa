#include <stdlib.h>
#include <stdbool.h>
#include <gmp.h>

#include <string.h>

/* Pregenerated series of small primes
const mpz_t[] first_primes;
 */

const size_t MAX_NUMBER_SIZE = 4096;

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
  /* Allocate a new private key ready-to-use
   */
  struct reesa_privkey* priv = malloc(sizeof(struct reesa_privkey));
  
  gmp_randstate_t state;
  gmp_randinit_default(state);
  
  mpz_init(priv->q);
  mpz_init(priv->p);

  void genprime(mpz_t, gmp_randstate_t);

  genprime(priv->q, state);
  genprime(priv->p, state);

  gmp_randclear(state);

  mpz_init(priv->modulus);
  mpz_mul(priv->modulus, priv->p, priv->q);

  mpz_t p1;
  mpz_init(p1);
  
  mpz_sub_ui(p1, priv->p, 1);

  mpz_t q1;
  mpz_init(q1);
  mpz_sub_ui(q1, priv->q, 1);

  mpz_init(priv->totient_modulus);
  mpz_mul(priv->totient_modulus, p1, q1);

  mpz_clear(q1);
  mpz_clear(p1);

  mpz_init_set_str(priv->public_exponent, "65537", 10);

  
  int inverse(mpz_t, const mpz_t, const mpz_t);
  inverse(priv->private_exponent, priv->public_exponent, priv->modulus);
  /* TODO check for error code */

  return priv;
}

int inverse(mpz_t rop, const mpz_t a, const mpz_t n) {
  /* Calculate the multiplicative inverse of a mod n 

     Used to generate the private key
   */

  mpz_t t;
  mpz_init_set_ui(t, 0);
  mpz_t r;  
  mpz_init_set(r, n);   
  mpz_t newt;
  mpz_init_set_ui(newt, 1);
  mpz_t newr;
  mpz_init_set(newr, a);
  mpz_t quotient;
  mpz_init(quotient);

  mpz_t temp;
  mpz_init(temp);
  mpz_t swapped;
  mpz_init(swapped);

  while (mpz_cmp_ui(newr, 0) != 0) {
    mpz_cdiv_q(quotient, r, newr);
    
    mpz_set(swapped, newt);
    mpz_mul(temp, quotient, newt);
    mpz_sub(newt, t, temp);
    mpz_set(t, swapped);
    
    mpz_set(swapped, newr);
    mpz_mul(temp, quotient, newr);
    mpz_sub(newr, r, temp);
    mpz_set(r, swapped);
  }

  if (mpz_cmp_ui(r, 1) > 0) {
    return 1;
  }

  if (mpz_cmp_ui(t, 0) < 0) {
    mpz_add(temp, t, n);
    mpz_set(t, temp);
  }
  
  mpz_set(rop, t);

  mpz_clear(r);
  mpz_clear(newt);
  mpz_clear(newr);
  mpz_clear(quotient);
  mpz_clear(temp);
  mpz_clear(swapped);
  mpz_clear(t);

  return 0;
}

void genprime(mpz_t rop, gmp_randstate_t state) {
  /* Generate a random number using GMP facilities 
     
     Validate the random number as a likely prime using GMP facilities
     (TODO: reimplement primality checking)
   */
  do {
    mpz_urandomb(rop, state, 128);
  } 
  while (mpz_probab_prime_p(rop, 25) == 0);
}


void gcd(mpz_t rop, const mpz_t cn, const mpz_t cm) {
  /* GMP has a GCD function defined, but we'll implement it again */
  int compare = mpz_cmp(cn, cm);
  if (compare == 0) {
    mpz_set(rop, cn);
    return;
  }

  mpz_t n;
  mpz_init_set(n, cn);

  mpz_t m;
  mpz_init_set(m, cm);

  mpz_t remainder;
  mpz_init(remainder);
  
  for (;;) {
    mpz_cdiv_r(remainder, n, m);
    
    if (mpz_cmp_ui(remainder, 0)) {
      mpz_clear(remainder);
      mpz_clear(n);
      mpz_set(rop, m);
      return;
    }
    
    mpz_set(n, m);
    mpz_set(m, remainder);
  }
}

void totient(mpz_t rop, const mpz_t n) {
  mpz_t i;
  mpz_init_set_ui(i, 1);
  mpz_set_ui(rop, 0);
  mpz_t gcd_temp;
  mpz_init(gcd_temp);

  while (mpz_cmp(i, n) < 0) {
    gcd(gcd_temp, i, n);

    if (mpz_cmp_ui(gcd_temp, 1)) {
      mpz_add_ui(rop, rop, 1);
    }

    mpz_add_ui(i, i, 1);
  }
  mpz_clear(gcd_temp);
  mpz_clear(i);
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
	      char* p, 
	      char* q, 
	      char* public_exponent, 
	      char* private_exponent, 
	      char* modulus, 
	      char* totient_modulus) {
  /* Write back our internal data structure into the given
     buffers.

     The buffers should be MAX_NUMBER_SIZE long
   */

  char* buf = malloc(MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->p);
  strncpy(p, buf, MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->q);
  strncpy(q, buf, MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->public_exponent);
  strncpy(public_exponent, buf, MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->private_exponent);
  strncpy(private_exponent, buf, MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->modulus);
  strncpy(modulus, buf, MAX_NUMBER_SIZE);

  mpz_get_str(buf, 10, priv->totient_modulus);
  strncpy(totient_modulus, buf, MAX_NUMBER_SIZE);

  free(buf);

  return 1;
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
