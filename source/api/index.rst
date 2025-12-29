================
API přihlašování
================

CAAIS poskytuje tři protokoly pro autentizaci uživatele. Pokud nemáte důvod zvolit jiný protokol, doporučujeme integraci protokolem OIDC.

.. toctree::
   :maxdepth: 1
   :numbered:

   oidc/index
   saml/index
   jip/index
   
.. Pro testování API či bližší pochopení API nabízíme nástroje v Pythonu dostupné v repozitáři…


Hlavní odlišnosti protokolů
===========================

Níže shrnujeme hlavní výhody a nevýhody jednotlivých protokolů.

OIDC
----

Výhody
......

- standardní a široce podporovaný protokol vycházející z OAuth 2.0
- jednoduchá a přátelská syntaxe
- údaje jsou předávány jako JSON Web Tokens (JWT)
- k dispozici autokonfigurace
- možnost využít `Keycloak <https://www.keycloak.org/>`_ jako middleware

Nevýhody
........

- nutnost přímé komunikace mezi AIS a CAAIS API, nikoli jen prostřednictvím prohlížeče
- různá úroveň ověření uživatele (level od assurance, LoA) vyžaduje vlastní přihlašovací URL


SAML 2.0
--------

Výhody
......

- standardní a široce podporovaný protokol, využívaný například NIA
- komunikace mezi AIS a CAAIS jen přes webový prohlížeč uživatele, nikoli napřímo
- k dispozici autokonfigurace
- možnost využít `Keycloak <https://www.keycloak.org/>`_ jako middleware

Nevýhody
........

- relativně komplikovaný protokol
- „těžkotonážní“ XML s množstvím jmenných prostorů a XML-DSig


JIP/KAAS legacy
---------------

Výhody
......

- AIS integrované vůči JIP/KAAS lze na CAAIS přepnout pouhou změnou konfigurace endpointů


Nevýhody
........

- proprietární protokol využívající SOAP
- konzervovaná množina údajů, které lze předávat
- mnoho inherentních omezení (jen jedna návratová URI, identifikace AIS pomocí jednoho registrovaného certifikátu atp.)


