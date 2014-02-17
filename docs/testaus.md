Testaus
===

Ohjelmalla on melko kattavat automaattiset testit. Ohjelman
automaattinen testaus tapahtuu kahdella tasolla.

Tässä dokumentissa käsitellään testauksen periaatteita yleensä,
käytettyjä testiarvoja ja niiden perusteluja on listattu varsinaisessa
testausympäristössä.

Yksikkötestit
---

Apufunktioita jotka kukin toteuttavat jonkin kokonaisen toiminnon,
yksikkötestataan. Yksikkötesteissä testataan joitakin mielenkiintoisia
ominaisuuksia toiminnosta. Toisaalta testataan myös joitain
virhetilanteita, joita tiedetään voivan syntyä. Kaikkia mielivaltaisia
vikatilanteita ei testata, esimerkiksi C-rutiineissa odotetaan ettei
niihin syötetä alustamattomia arvoja.

Integraatiotestit
---

Kokonaisia käyttäjälle tarjottavia kokonaisuuksia testataan
integraatiotesteillä. Koska ohjelman ydintoiminnot ovat datan
muunnoksia, integraatiotesteissä testataan kiertomatkoja. Näillä
varmistetaan algoritmin tärkein ominaisuus eli kyky muuntaa kerran
kryptattu data takaisin luettavaan muotoon.

Integraatiotesteissä testataan lisäksi ohjelman virheellisestä
käytöstä aiheutuvia virheitä, jotka ohjelman pitäisi huomata ennen
syvälle C-rutiineihin menemistä.

Testien tuloksia
---

Uutta ominaisuutta kehittäessä automaattitestit kehitettiin
käsintestauksen pohjalta. Vain tiedostokäsittelyssä testit tehtiin
ennen varsinaisen toiminnon loppuun kehittämistä.

Automaattitesteillä varmistetaan siis, että vanhat ominaisuudet eivät
mene pahasti rikki uusia kehittäessä.

Eräs mainittavan arvoinen testitulos oli kun syötin salausalgoritmille
hankalan syötteen: testaustiedoston itse. Tällä testillä paljastui
vakava puute algoritmissa, joka pakotti minut toteuttamaan
minimaalisen padding-menetelmän.