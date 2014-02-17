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

Puutteita
---

Ohjelmaan en ole vielä ehtinyt toteuttamaan digitaalisia
allekirjoituksia käyttäen ohjelman avainpareja.

Salaus ei ole mitenkään vahvaa. Avaimet ovat pienikokoisia, ne
generoidaan pienestä ja ennakoitavasta satunnaisavaruudesta ja
salausmenetelmän muissa osissa ei ole huomioitu yleisesti tunnettuja
hyökkäysreittejä.
