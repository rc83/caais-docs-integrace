=============================
Integrace nového AIS na CAAIS
=============================

*Tato kapitola poskytuje základní přehled integrace AIS na CAAIS pro garanty AIS a případně též analytiky a architekty AIS.*

On-boarding
===========

Chcete-li integrovat svůj AIS na CAAIS, kontaktujte nás prostřednictvím `Service Desk DIA`_. Pro urychlení komunikace tiket pojmenujte „Integrace AIS {zkratka AIS} do CAAIS“. Následně se domluvíme na on-line schůzce, kde dořešíme podrobnosti integrace. Výstupem schůzky bude předání přístupu do :ref:`integračního prostředí <si:env:int>` s konfigurací na míru vašemu AIS.

Osvědčuje se, pokud se schůzky mohou účastnit

- věcný správce,
- projektový manažer,
- analytik modelu oprávnění,
- vývojář.

Návrh modelu oprávnění
======================

Činnostní a aplikační role
--------------------------

CAAIS rozlišuje *činnostní role*, které definuje základní registr práv a povinností (RPP), a *přístupové role*, které si definuje AIS v CAAIS podle svých potřeb. Model oprávnění v AIS může s výhodou využívat oba typy rolí současně. AIS se při přihlášení uživatele dozví všechny jeho činnostní role a všechny jeho přístupové role definované tímto AIS.

Správce agendy v RPP a správce AIS v CAAIS přiděluje role vždy jen na instituce (úřady). Je už plně v pravomoci každé instituce, jak role jí svěřené přidělí prostřednictvím svého lokálního administrátora CAAIS konkrétním uživatelům.

Přihlašování bez role
---------------------

Přístupové role se dají využívat jako běžné aplikační role, nebo k řízení přístupu uživatelů (například s činnostními rolemi) do aplikace.

Ve výchozí konfiguraci dovoluje CAAIS přihlášení do AIS jen těm uživatelům, kteří mají přiřazenu alespoň jednu přístupovou roli daného AIS. Konfiguraci lze však upravit tak, aby se mohli přihlašovat všichni uživatelé instituce, která má přiřazenu alespoň jednu přístupovou role; anebo aby se mohli přihlašovat všichni uživatelé bez ohledu na přidělení přístupové role. Poslední možnost je vhodná pro AIS, kterým pro základní aplikační roli postačuje autentizace uživatele – příkladem buď Service Desk DIA, kde tiket může založit po autentizaci kdokoli.

Identifikátor uživatele
-----------------------

Uživatel se vždy hlásí za určitou instituci (úřad) svým profilem. Jméno profilu je však pouze transientní identifikátor. Pokud potřebujete uchovávat údaje k profilu uživatele na straně AIS, použijte BSI profilu ve formátu UUID jako persistentního identifikátoru.

Potřebujete-li uživatele namapovat do AIFO prostoru své agendy, připravujeme podporu pro předávání úložky AIFO v základních registrech (IS ORG).

Identifikátor instituce (subjektu)
----------------------------------

Pro praktické potřeby je jednoznačným identifikátorem instituce *coalesce(OVMID, IČO)*, kde OVMID je identifikátor orgánu veřejné moci přebíraný z registru práv a povinností (RPP) a IČO identifikátor organizace z registru osob (ROS). Oba identifikátory pocházení z téhož datového prostoru, a nemůže tak dojít ke konfliktu.

- Instituce, které nejsou orgány veřejné moci, nemají OVMID přiděleno.
- Většina orgánů veřejné moci má shodné OVMID a IČO.
- Některé orgány veřejné moci mají pouze OVMID.


Návrh architektury
==================

Protokoly
---------

CAAIS podporuje dva standardní protokoly :ref:`OIDC <api_oidc>` a :ref:`SAML 2.0 <api_saml>`. Integrace protokolem OIDC je poměrně přímočará; nemáte-li zásadní důvod pro SAML 2.0, **doporučujeme použít protokol OIDC**.

Pro úplnost zmiňme, že CAAIS podporuje i proprietární protokol :ref:`JIP/KAAS legacy <api_jip>`, ale jeho použití pro novou integraci nemá opodstatnění.


Keycloak jako middleware
------------------------

Pokud AIS potřebuje sdružit různé poskytovatele identity (například CAAIS a interní), může být výhodné použít `Keycloak <https://www.keycloak.org/>`_ jako middleware. S CAAIS jej lze propojit protokoly OIDC nebo SAML 2.0.

Další využití Keycloak je jako SAML proxy, když potřebujete funkcionalitu SAML, kterou CAAIS (zatím) nepodporuje, například mapování atributů.


Rozhraní CMS a Internet
-----------------------

CAAIS je pro AIS a uživatele dostupný na dvou rozhraní: Centrální místo služeb a Internet. V konfiguraci AIS se volí, z jakých rozhraní může přistupovat uživatel. (Pro AIS je CAAIS dostupný v CMS vždy.)

Sám CAAIS běží v CMS a je připraven na běh v ostrovním režimu.

Poskytovatelé identity CAAIS-IdP & NIA
--------------------------------------

V produkčním prostředí jest lze využít pro přihlášení různé IdP – aktuálně interní CAAIS-IdP a NIA – Identitu občanu. Z pohledu AIS je volba IdP transparentní. V konfiguraci AIS však lze povolit jen určité IdP.

AIS současně ve své konfiguraci požaduje, s jakou minimální úroveň záruky (LoA) ověření se může uživatele přihlásit. Ve většině případů vyhovuje *značná (substantial)* dle eIDAS.


Fáze integrace
==============

Vývoj a integrační testování
----------------------------

Vývoj a integrační testování probíhají na integračním prostředí test-ext. Zapojen je především dodavatel AIS a správce integračního prostředí CAAIS z DIA, který připraví konfiguraci AIS v CAAIS a předá ji dodavateli. Používají se fiktivní uživatelské účty a testovací certifikáty. Spolupráce dalších stran není nutná.


Uživatelské testování
---------------------

Testování reálnými uživateli pomocí jejich reálných účtů probíhá vůči testovací či školicí konfigurace AIS v *produkčním CAAIS*. Je vhodné nás o chystaném provozu proti produkčnímu CAAIS informovat a případně si domluvit schůzku k ujasnění postupu.

Školicí konfiguraci AIS v produkčním CAAIS zakládá lokální administrátor CAAIS instituce (úřadu), která AIS provozuje. Při tom nastaví pověřenému uživateli ze své instituce, obvykle technickému správci, roli garanta AIS pro správu založené konfigurace. Ten následně ve spolupráci s dodavatelem konfiguraci AIS dokončí.

Součástí konfigurace je i registrace :ref:`certifikátů pro komunikaci mezi AIS a CAAIS<si:certs:ais>`.

Po nastavení konfigurace jest lze oslovit lokální administrátory institucí, které se testování účastní, aby přidělili uživatelům patřičné přístupové a činnostní role. Žádost o přidělení rolí musí být dostatečně specifická: Měla by obsahovat název a zkratku konfigurace AIS (rozlišení produkce a testování) a názvy přidělovaných rolí. Lokální administrátory CAAIS většinou oslovíte prostřednictvím svého koordinátora testování v dané instituci.


Pre-produkce a produkce
-----------------------

Nastavení produkční konfigurace AIS v CAAIS probíhá obdobně jako školicí konfigurace. Informujte nás prosím s dostatečným předstihem, kdy se chystáte produkční provoz spustit, abychom byli připraveni stran uživatelské podpory.

V této fázi je velice důležitá přesná a úplná komunikace s budoucími uživateli AIS (institucionálními i lidmi), se kterou vám rádi pomůžeme. Zejména v roce 2026 bude pro mnoho institucí CAAIS ještě poměrně novým systémem, se kterým teprve nabírají zkušenosti.


Integrační (testovací) prostředí
================================

:ref:`Integrační prostředí test-ext<si:env:int>` slouží pro ověření integrace AIS vůči CAAIS. Jakmile projevíte zájem o integraci AIS na CAAIS, připravíme vám testovací konfiguraci a předáme vám ji do správy skrze fiktivního uživatelského účtu. Pro úvodní nastavení funkční konfigurace potřebujeme znát:

- název AIS,
- zkratku AIS (slouží též jako identifikátor konfigurace v autentizačních protokolech; doporučujeme omezit na ASCII znaky),
- protokol,
- URL endpointu po přihlášení,
- URL endpointu po odhlášení,
- certifikát či žádost o certifikát,
- seznam rolí.

Hodnoty může doplňovat a měnit kdykoli později sami jako správci konfigurace. Představu o nastavení konfigurace AIS vám dají :ref:`tutorial_oidc` a :ref:`tutorial_saml`. Integrační prostředí slouží i jako testovací pískoviště ve vztahu k ověřování voleb konfigurace.

Pro testovací prostředí není nutné zařizovat komerční certifikáty. Na základě žádosti o certifikát vám jej dokážeme vystavit prostřednictvím neveřejné certifikační autority CAAIS.


.. admonition:: Testování AIS
   :class: warning

   Integrační prostředí neslouží k extenzivnímu testování samotného AIS. Tomu odpovídá i omezená množina údajů dostupná v tomto prostředí.
   Týká se to zejména institucí (subjektů), činnostních rolí a počtu uživatelů.


Produkční prostředí
===================

Nastavení :ref:`produkčního prostředí <si:env:prod>` provádí primárně garant AIS ve spolupráci s dodavatelem. Pro napojení AIS na CAAIS je nutné si obstarat patřičný :ref:`komerční serverový certifikát <si:certs>`.

Produkční prostředí CAAIS je dostupné jak z CMS, tak z Internetu. Není nutné žádat o úpravy firewallu na straně CAAIS, ni nám poskytovat IPv4 a IPv6 rozsah vašeho AIS.


.. admonition:: Platnost certifikátu
   :class: info
   
   Na straně AIS je třeba hlídat platnost certifikátu registrovaného v CAAIS a před jeho exspirací jej včas obměňovat.

Školicí prostředí AIS
---------------------

Počet konfigurací AIS v produkčním CAAIS neomezujeme. Pokud máte školicí prostředí AIS, lze pro něj vytvořit samostatnou konfiguraci v CAAIS.

Oslovení uživatelů AIS
----------------------

Vedle informací o samotném AIS je nutné uživatele též seznámit, o jaká oprávnění k přístupu do AIS potřebují a jak si o ně mohou zažádat. Nabízíme metodickou podporu při formulování této části sdělení.


Často kladené otázky
====================

*zatím prázdné*

Další zdroje
============

- :ref:`tutorial_oidc`
- :ref:`tutorial_saml`
- :ref:`api_oidc`
- :ref:`api_saml`


Kontakt a podpora
=================

Pokud máte v úmyslu integrovat svůj AIS na CAAIS, kontaktujte nás prosím přes `Service Desk DIA`_. Pro urychlení komunikace tiket pojmenujte „Integrace AIS {zkratka AIS} do CAAIS“. Následně se domluvíme na on-line schůzce k dořešení podrobností integrace.

.. _Service Desk DIA: https://portal.szrcr.cz/ 
