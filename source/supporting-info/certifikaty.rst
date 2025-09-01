.. _si:certs:

===========
Certifikáty
===========

Certifikáty se v CAAIS používají jednak jako druhý faktor při autentizaci uživatele prostřednicvím CAAIS IdP, jednak pro zabezpečení komunikace mezi připojeným AIS a CAAIS.

Uživatel
========

Pokud uživatel využívá CAAIS IdP a potřebuje se přihlašovat na úrovni záruky značná, musí mít v CAAIS IdP registrovaný autentizační certifikát vydaný :ref:`podporovanou certifikační autoritou <si:ca>`.


Připojený AIS
=============

Podle zvoleného protokolu jsou využívány certifikáty AIS následujícím způsobem:

- **OIDC** — autentizace AIS v rámci mTLS spojení
- **SAML 2.0** — (i) podpis požadavku a (ii) dešifrování assertion v odpovědi
- **JIP/KAAS legacy** — identifikace AIS a jeho autentizace v rámci mTLS spojení


.. _si:ca:

Podporované certifikační autority
=================================

Pro všechny účely lze v CAAIS používat jen certifikáty vydané **certifikační autoritou uznávanou v rámci eIDAS**. Aktuálně jsou v CAAIS registrovány certifikáty následujících certifikačních autorit:

- eIdentity
- I. CA
- Národní certifikační autorita
- Postsignum

Další certifikační autority uznávané v rámci eIDAS přidáme na žádost dle potřeby. Self-signed certifikáty, certifikáty vydané interní certifikační autoritou úřadu či správou základních registrů nelze použít.


Pro *integrační testování* v prostředí test-ext lze navíc používat i testovací certifikáty, pokud je některá výše uvedená certifikační autorita nabízí. Další možností je nechat si vystavit testovací certifikáty interní certifikační autoritou CAAIS na základě Certificate Signing Request (CSR), který nám zašlete.
