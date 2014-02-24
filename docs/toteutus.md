
Toteutus
===

Olen tyytyväinen ohjelman tehokkuuteen. Valmiiseen ohjelmaan päätyneet
tehokkuutta mitoittavat algoritmit ovat itse asiassa tehokkaampia kuin
mitä määrittelyssä on annettu:

- Avaingeneraatiossa ei oikeasti käytetä totienttifunktiota, vaan se
  lasketaan suoraan hyödyntäen alkulukujen ominaisuuksia.

- Salauksessa ja purussa käytettävä modulaarinen
  eksponentiointifunktio on tehostettu O(log e)-tehokkuusluokkaan,
  koska O(e) olisi ollut sietämättömän hidas ohjelmassa käytetyillä
  sinänsä pienikokoisilla 128-bittisillä avaimilla.

Eksponentoinnin tehokkuus pseudokoodina (neliöintimenetelmä):

    def mod_pow(base, exp, modulus):
        result = 1
        base = base mod modulus

        while exp > 0:
            if exp mod 2 == 1:
	        result = (result*base) mod modulus
	    exp = exp >> 1 # exp = exp / 2
	    base = (base*base) mod modulus

        return result

exp:stä häviää yksi bitti joka silmukassa, joten silmukkaa ajetaan
`ceil(log_2 exp)` kertaa.

Puutteita
---

Ohjelmaan en ole vielä ehtinyt toteuttamaan digitaalisia
allekirjoituksia käyttäen ohjelman avainpareja.

Salaus ei ole mitenkään vahvaa. Avaimet ovat pienikokoisia, ne
generoidaan pienestä ja ennakoitavasta satunnaisavaruudesta ja
salausmenetelmän muissa osissa ei ole huomioitu yleisesti tunnettuja
hyökkäysreittejä.
