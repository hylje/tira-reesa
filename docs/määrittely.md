Minkä ongelman ratkaiset ja millä tietorakenteella tai algoritmilla
===

Ratkaisen yksityisen viestinnän ongelmat lohkosalauksella.

Keskeinen algoritmi on RSA, johon liittyy avaingeneraatiossa muitakin
algoritmeja kuten Erastoteneen seula ja Eulerin Φ-funktio.

Maininnan arvoisia tietorakenteita ei sisälly toteutukseen.

Miten tehokkaasti toteutuksesi tulee ongelman ratkaisemaan (aika- ja tilavaativuudet)
===

Salauksen ja purun tavoitetehokkuus on aikavaativuudeltaan O(e) jossa
e=salausavaimen kyseinen eksponentti. Salauksessa ja purussa käytetään
eri eksponentteja. Tehokkaampiakin potenssilaskun algoritmeja on,
mutta aloitan yksinkertaisesta. Tilavaativuudeltaan kuitenkin vakio.

Salausavaimen generoinnissa tavoitetehokkuuteen päädytään seuraavasti:

Satunnaisluvut
---

n kappaletta noin 256-bittisiä satunnaisia kokonaislukuja: 

### Aika

n * O(256) => O(n)

### Tila

O(1) 

Satunnaislukuja generoidaan vain yksi kerrallaan, koska niitä tarvitaan
yhtäaikaa korkeintaan 2

Alkulukujen valitseminen
---

joista valitaan 2 kappaletta, p ja q, kohtuullisen todennäköisiä alkulukuja: 

### Aika

n * O(k * log2 p * log log p * log log log p)

jossa k on alkulukutestauksien määrä ja p on kokonaisluku, p>>n

### Tila

O(1)

Φ(p*q):n laskeminen
---

### Aika

O(m log m) jossa m=p*q, m>>p
(Tästä on tehokkaampiakin ratkaisuja, mutta tämä on yksinkertainen)

### Tila
 
O(1)

Julkinen ja salainen eksponentti
---

### Aika

O(n log n) jossa
n < Φ(p*q) 
=> n < p*q
=> n < m 
=> n log n < m log m

### Tila

O(1)

Näistä merkittävimmät aikavaativuudet ovat totienttifunktiolla Φ.

Tilavaativuus on puolestaan vakio.


Mitä lähdettä käytät. Mistä ohjaaja voi ottaa selvää tietorakenteestasi/algoritmistasi
===

Käytettävien algoritmien tietoja olen hakenut muun muassa:

http://en.wikipedia.org/wiki/RSA_(algorithm)

http://en.wikipedia.org/wiki/Euler%27s_totient_function
- http://math.stackexchange.com/questions/632837/time-complexity-of-euler-totient-function

http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers