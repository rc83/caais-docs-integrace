.. _si:certs:

===========
Certifikáty
===========

Certifikáty se v CAAIS používají jednak jako druhý faktor při autentizaci uživatele prostřednicvím CAAIS IdP, jednak pro zabezpečení komunikace mezi připojeným AIS a CAAIS.

Uživatel
========

Pokud uživatel využívá CAAIS IdP a potřebuje se přihlašovat na úrovni záruky značná, musí mít v CAAIS IdP registrovaný autentizační certifikát vydaný :ref:`podporovanou certifikační autoritou <si:ca>`. Z důvodu bezpečnosti a certifikačních politik *nelze* k autentizaci používat certifikát pro kvalifikovaný podpis.


Připojený AIS
=============

Podle zvoleného protokolu jsou využívány certifikáty AIS následujícím způsobem:

.. - **OIDC** — autentizace AIS v rámci mTLS spojení
.. - **SAML 2.0** — (i) podpis požadavku a (ii) dešifrování assertion v odpovědi
.. - **JIP/KAAS legacy** — identifikace AIS a jeho autentizace v rámci mTLS spojení

.. list-table:: Využití cerfitikátů autentizačními protokoly
   :header-rows: 1

   * - Protokol
     - Typ certifikátu
     - Využití
     - Poznámka      
   * - OIDC
     - autentizační
     - autentizace AIS v rámci mTLS spojení
     - - alespoň jeden platný certifikát
   * - SAML 2.0
     - podepisovací
     - podpis požadavku
     - - právě jeden platný certifikát
       - může být shodný s šifrovacím
   * - SAML 2.0
     - šifrovací
     - zašifrování atributů v odpovědi
     - - právě jeden platný certifikát
       - může být shodný s podepisovacím
   * - JIP/KAAS
     - autentizační
     - identifikace a autentizace AIS v rámci mTLS spojení
     - - alespoň jeden platný certifikát
       - certifikát nesmí být registrován v jiné konfiguraci AIS



.. _si:ca:

Podporované certifikační autority
=================================

Pro všechny účely lze v CAAIS používat jen certifikáty vydané **certifikační autoritou uznávanou v rámci eIDAS**. Aktuálně jsou v CAAIS registrovány certifikáty následujících certifikačních autorit:

- eIdentity
- I. CA
- Národní certifikační autorita
- Postsignum

Další certifikační autority uznávané v rámci eIDAS přidáme na žádost dle potřeby. Self-signed certifikáty, certifikáty vydané interní certifikační autoritou úřadu či správou základních registrů nelze použít.


Pro *integrační testování* :ref:`v prostředí test-ext <si:env:int>` lze navíc používat i testovací certifikáty, pokud je některá výše uvedená certifikační autorita nabízí. Další možností je nechat si vystavit testovací certifikáty interní certifikační autoritou CAAIS na základě Certificate Signing Request (CSR), který nám zašlete.
