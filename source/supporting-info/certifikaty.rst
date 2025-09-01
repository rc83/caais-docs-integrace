.. _si:certs:

===========
Certifikáty
===========

Certifikáty se v CAAIS používají jednak jako druhý faktor při autentizaci uživatele prostřednicvím CAAIS IdP, jednak pro zabezpečení komunikace mezi připojeným AIS a CAAIS.


.. _si:certs:user:

Uživatel
========

Pokud uživatel využívá CAAIS IdP a potřebuje se přihlašovat na úrovni záruky značná, musí mít v CAAIS IdP registrovaný autentizační certifikát vydaný :ref:`podporovanou certifikační autoritou <si:ca>`. Z důvodu bezpečnosti a certifikačních politik *nelze* k autentizaci používat certifikát pro kvalifikovaný podpis.


.. _si:certs:ais:

Připojený AIS
=============

Podle zvoleného protokolu jsou využívány certifikáty AIS následujícím způsobem:

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
   * - editační WS 1.1
     - autentizační
     - autentizace IdM v rámci mTLS spojení
     - - alespoň jeden platný certifikát
       - postačuje certifikát v libovolné konfiguraci AIS


.. _si:certs:ais:issue:

Postup vydání certifikátu pro AIS
---------------------------------

Na vydání certifikátu pro AIS spolupracuje obvykle několika stran a ne všichni musí být s tímto procesem dokonale seznámeni. Přinášíme proto stručný postup.

1. **Vytvoření páru klíčů** – soukromého a veřejného. Jelikož soukromý klíč nesmí opustit bezpečné prostředí, tuto činnost zpravidla provádí poskytovatel služby (správce běhového prostředí). Použité kryptografické algoritmy musí vyhovovat certifikační politice zvolené certifikační autority a doporučení NÚKIB (RSA 3072, RSA 4096, P-256, P-384 atp.).

#. **Vytvoření žádosti o vydání certifikátu** – Certificate Signing Request (CSR). Žádost připraví opět poskytovatel služby, neboť musí být podepsána soukromým klíčem. Žádost obsahuje hodnoty několika atributů. Atribut *Common Name* je vždy povinný a další atributy uvedené v tabulce níže jsou doporučené. Vyžadované a povolené atributy pak plynou z politiky zvolené certifikační autority. Hodnoty atributů sdělí poskytovateli služby technický správce AIS.

  .. list-table:: Atributy certifikátu a žádosti o certifikát
     :widths: 22 80
     :header-rows: 1

     * - Atribut
       - Popis
     * - CN (Common Name)
       - Identifikace klientského systému. Měl by to být název připojovaného AIS, případně jeho zkratka či doménové jméno, pod kterým je AIS provozován. CAAIS tuto hodnotu (zatím) nevyužívá.
     * - O (Organization)
       - Žadatel o certifikát. Obvykle provozovatel AIS, například příslušné ministerstvo.
     * - OU (Organization Unit)
       - Dle zvyklostí provozovatele, například odbor technického správce AIS. Volitelné.
     * - C (Country)
       - CZ

  Samotná žádost již neobsahuje žádné citlivé informace a lze ji dále předat otevřeným kanálem žadateli o certifikát.

3. **Vydání certifikátu.** Žadatel o certifikát převezme žádost o certifikát, zkontroluje ji (včetně otisku veřejného klíče) a v souladu s rámcovou smlouvou, kterou má jeho instituce uzavřena s vybranou certifikační autoritou, jí žádost postoupí.

#. **Instalace certifikátu.** Po získání certifikátu jej žadatel o certifikát předá poskytovateli služby, aby jej mohl instalovat do běhového prostředí AIS, a správci konfigurace AIS v CAAIS, aby jej mohl zaregistrovat. Certifikát neobsahuje citlivé informace, a lze jej tak předat otevřeným kanálem.

.. admonition:: Typ certifikátu
   :class: info

   AIS potřebuje klientský certifikát pro server. U certifikačních autorit se lze setkat s pojmenováním komerční serverový certifikát. Není nutné pořizovat doménový certifikát.


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


.. _si:certs:faq:

Často kladené otázky
====================

.. _si:certs:faq-1:

**Otázka 1: Zkoušel jsem přidat certifikát QCA k uživateli a při tom jsem zjistil, že máte v seznamu autorit vydávající certifikáty špatně uvedenou autoritu pro QCA certifikáty PostSignum – chybí CN=PostSignum QCA 4.**

Kvalifikované certifikáty *nelze* pro autentizaci uživatelů použít, jsou určeny výhradně pro kvalifikovaný podpis dle eIDAS. Kvalifikované certifikáty neobsahují hodnotu Client Authentication (OID 1.3.6.1.5.5.7.3.2) v atributu Extended Key Usage (EKU). Toto omezení dané certifikační politikou brání zneužití kvalifikovaného podpisu. Je nutné použít certifikáty vydané jako komerční; v případě Postsignum se jedná o certifikáty podepsané `mezilehlým certifikátem`_ CN=PostSignum Public CA 4 či CN=PostSignum Public CA 5 (údaj pro rok 2025). Tyto mezilehlé certifikáty CAAIS rozpoznává.

.. _mezilehlým certifikátem: https://www.postsignum.cz/certifikaty_autorit.html
