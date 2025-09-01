Příprava: Vygenerování autentizačního certifikátu AIS
=====================================================

Nejjednodušší cesta je poslat nám žádost o certifikát (certificate signing request) jako soubor csr. Alternativně můžete použít komerční certifikát stejného typu jako na produkčním prostředí, anebo testovací certifikát týchž certifikačních autorit (nabízí se zejména PostSignum).

Vytvoření CSR pomocí `openssl`
------------------------------

Nejprve vygenerujte privátní klíč. Můžete využít algoritmus RSA (1a) o délce klíče 2048, 3072 či 4096 bitů, anebo ECDSA (1b) o délce klíče 256, 383 či 521 bitů. 

.. code:: bash

  (1a) $ openssl genrsa -out key.pem 2048
  (1b) $ openssl genpkey -algorithm ec -pkeyopt ec_paramgen_curve:P-256 -out key.pem

Následně vygenerujte (2) žádost o vystavení certifikátu (CSR soubor):

.. code:: bash

  (2)  $ openssl req -new -key key.pem -out server.csr \
           -subj "/C=CZ/O=Ministerstvo administrativních záležitostí/CN=forms.example.gov.cz"

Hodnotu parametru `-subj` upravte podle svého (testovacího) AIS; `CN` by mělo odpovídat plně kvalifikovanému doménovému jménu (FQDN) serveru AIS, se kterým bude testovací prostředí CAAIS komunikovat. Zkontrolujte vytvořenou žádost (3).  

.. code:: bash

  (3)  $ openssl req -text -noout -in server.csr | grep Subject:

Soubor `server.csr` nám pošlete, abychom vám mohli vytvořit testovací certifikát. Alternativně jej můžete použít k získání (testovacího) certifikátu od komerční certifikační autority.

Alternativa: Testovací certifikát od PostSignum
-----------------------------------------------

Žádost o certifikát (CSR soubor) nahrajte na `stránkách PostSignum <https://www.postsignum.cz/testovaci_certifikat.html>`_. Vyberte možnost *Komerční serverový certifikát (VCA)*. Vyplňte *název certifikátu* jako plně kvalifikované doménové jméno (FQDN) serveru AIS, se kterým bude testovací prostředí CAAIS komunikovat. V našem příkladu `forms.example.gov.cz`. Dále vyplňte *e-mail*, kam bude následně odkaz ke stažení testovacího certifikátu doručen a formulář odešlete.

Poznámka: Generování certifikátu PostSignum pro ECDSA klíče aktuálně (listopad 2024) selhává.
