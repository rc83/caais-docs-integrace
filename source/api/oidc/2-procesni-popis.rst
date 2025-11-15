=========================================
Proces přihlášení a odhlášení pomocí OIDC
=========================================

V OIDC jsou definovány čtyři základní role účastnící se komunikace, které se pro případ CAAIS překládají následovně:

  - Resource Owner = uživatel,
  - Relying Party = AIS,
  - OpenID Provider = CAAIS,
  - Identity Provider = CAAIS-IdP či NIA.
  
Proces přihlášení
=================

CAAIS podporuje proces přihlášení `Authorization Code Flow (ACF) <oidc_acf_>`_. Z pohledu AIS má proces autentizace protokolem OIDC tři hlavní části:

  1. AIS poskytne uživateli (jeho webovému prohlížeči) pro přihlášení parametrizovanou URL na *autorizační endpoint* CAAIS.
  #. Po úspěšném přihlášení přesměruje CAAIS uživatele (jeho webový prohlížeč) zpět na požadovaný endpoint AIS; součástí přesměrování je předání parametru ``code``.
  #. AIS přímo komunikuje s CAAIS API na *token endpointu*, aby vyměnil ``code`` za *identity token* obsahující podrobnosti o přihlášeném uživateli. CAAIS vydá *identity token*, jen pokud je požadavek AIS ověřený.

.. _oidc_acf: https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth
  
Podrobněji zachycuje proces autentizace následující diagram:

.. figure:: images/diagram-oidc.png
   :width: 1000px

   Diagram autentizace uživatele protokolem OIDC.
   
   
1. Uživatel otevře webovou stránku AIS.

#. Pokud AIS zjistí, že není uživatel přihlášen (nemá v AIS aktivní sezení), přesměruje uživatele na *autorizační endpoint* CAAIS. URL přesměrování obsahuje parametr ``return_uri``. Na přihlašovací stránce CAAIS si uživatel zvolí způsob přihlášení a zadá přihlašovací údaje.

#. Systém CAAIS ověří, že autentizační metoda vybraná uživatelem splňuje úroveň LoA, která je pro daný AIS nakonfigurována v CAAIS. Provádí-li se autentizace pomocí interního CAAIS-IdP, komponenta CAAIS-IdP ještě navíc ověří správnost zadaných přihlašovacích údajů uživatele vůči uloženým údajům.

#. Pokud je autentizace úspěšná, provede CAAIS načtení informací o uživateli ze své databáze. Následně se v CAAIS na základě přístupových rolí přidělených uživateli ověří, zda je oprávněn přistoupit do AIS. Pokud ano, pokračuje se dalším krokem. Jinak se uživateli zobrazí hláška o zamítnutí přístupu.

#. CAAIS vygeneruje OIDC odpověď obsahující ``code``.

#. A uživatel je s touto odpovědí přesměrován zpět na endpoint AIS odpovídající hodnotě parametru ``return_uri`` z kroku 2. 

#. V systému AIS se zpracuje OIDC odpověď obsahující ``code``.

#. Následně jej AIS odešle přes HTTP požadavek na *token endpoint* na CAAIS, kde se ověří právě získaným ``code`` parametrem a svým ověřovacím certifikátem. CAAIS zkontroluje obdržený ``code`` parametr a autentizační údaje.

#. Pokud jsou validní, CAAIS odešle AIS *access token* a *identity token* uživatele.

#. AIS ověří, že identity token obdržený v odpovědi je validní (podpis a časové značky), a na základě informací o uživateli získaných z odpovědi posoudí, zda umožní uživateli přístup.


Autentizace požadavku AIS vůči CAAIS
------------------------------------

Než CAAIS vydá *access token* a *identity token* (kroky 8–10 v Diagramu), ověřuje, že požadavek je oprávněný. Standardně se to děje ověřením autentizačního certifikátu AIS při navázání mTLS spojení na *token endpoint*. Certifikát AIS musí být zaregistrován v konfiguraci AIS v CAAIS a musí být vydán podporovanou certifikační autoritou (podrobnosti v části :ref:`si:certs`).

Vedle toho lze ověření doplnit i o Proof Key for Code Exchange (PKCE; :rfc:`7636`) flow. Pak se v kroku 2 posílá v rámci přesměrování na *autentizační endpoint* navíc parametr `code_challenge` a v kroku 8 na *token endpoint* parametr `code_verifier`. Hodnoty `code_challenge` a `code_verifier` si musejí odpovídat – hodnota `code_challenge` je SHA256 hash (náhodné) hodnoty `code_verifier`.


Uchování stavu během přihlašování
---------------------------------

Hodnota parametru ``return_uri`` musí být předem registrována v konfiguraci AIS v CAAIS (white list). Samotnou URL tak nelze použít k zachycení stavu či ad hoc parametrizace akce, ke které má dojít po přihlášení na straně AIS. Pokud AIS potřebuje během přihlašování udržet stav, musí použít OIDC parametr ``state``.



Proces odhlášení
================

1. Uživatel zvolí odhlášení v AIS.

#. AIS ukončí své sezení uživatele.

#. AIS přesměruje uživatele na *endpoint ukončení sezení* v CAAIS. URL přesměrování obsahuje parametr ``post_logout_redirect_uri``.

#. Uživateli je v CAAIS nabídnuta možnost ukončit single sign-on (SSO) sezení v CAAIS. Uživatel může a nemusí SSO sezení ukončit.

#. Uživatel je přesměrován zpět do AIS na adresu odpovídající hodnotě parametru ``post_logout_redirect_uri`` z kroku 3.

#. AIS informuje uživatele, že byl z AIS odhlášen.

Rozhodnutí uživatele v kroku 4 nemá přímý dopad na AIS, který proto rozhodnutí uživatele nijak neřeší. Případné nové přihlášení uživatele do AIS je iniciováno bez rozdílu, zda uživatel ukončil SSO sezení v CAAIS.


Uchování stavu během odhlašování
--------------------------------

Hodnota parametru ``post_logout_redirect_uri`` musí být předem registrována v konfiguraci AIS v CAAIS (white list). Samotnou URL tak nelze použít k zachycení stavu či ad hoc parametrizace akce, ke které má dojít po odhlášení na straně AIS. Pokud AIS potřebuje během odhlašování udržet stav, musí použít OIDC parametr ``state``.


Úroveň záruk
============

`Nařízení eIDAS <eidas_>`_ rozlišuje tři úrovně záruky (level of assurance, LoA) ověření uživatele: nízká (low), značná (substantial) a vysoká (high). AIS si může v konfiguraci definovat, jakou minimální záruku ověření uživatele vyžaduje. CAAIS pak při přihlášení uživatele do AIS garantuje, že je využit přihlašovací prostředek tuto nebo vyšší záruku poskytující.

Skutečná úroveň záruky se však protokolem OIDC nepředává. Pokud ve výjimečném případě potřebuje AIS rozlišovat přihlášení na různé úrovni ověření uživatele, musí nabídnout více odkazů k přihlášení, odvolávající se na příslušné konfigurace AIS v CAAIS.

.. _eidas: https://eur-lex.europa.eu/legal-content/CS/TXT/?uri=CELEX:32014R0910
