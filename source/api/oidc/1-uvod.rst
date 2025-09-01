====
Úvod
====

Účelem tohoto dokumentu je popsat technické detaily uživatelské autentizace do agendových informačních systémů (AIS), které jsou registrovány v systému CAAIS.

Uživatel se přihlašuje do systému s využitím CAAIS-IdP (modul interního IdP CAAIS), který zde plní funkci autentizačního informačního systému dle `§ 56a zákona č. 111/2009 Sb., o základních registrech <zr_>`_. Alternativně se může uživatel přihlašovat pomocí NIA (identitu občana), zřízenou `zákonem č. 250/2017 Sb., o elektronické identifikaci <nia_>`_. Pro AIS je zcela transparentní, který IdP byl v CAAIS použit.

.. _zr: https://www.e-sbirka.cz/sb/2009/111#par_56a
.. _nia: https://www.e-sbirka.cz/sb/2017/250

Komunikace a předávání údajů o uživateli probíhá pomocí `protokolu OIDC <oidc_core_>`_, který se využívá pro výměnu autentizačních a autorizačních dat. V terminologii OIDC vystupuje CAAIS v roli poskytovatele OpenID (OpenID Provider) a AIS v roli spoléhající se srany (Relying Party). Prostřednictvím OIDC protokolu předává CAAIS AIS definovanou sada atributů uživatele (viz kapitola :ref:`oidc:atributy`), která je podmnožinou všech atributů, které jsou o uživateli (profilu) v systému CAAIS evidovány.


CAAIS v souladu s `doporučením <oidc_dicover_conf_>`_ poskytuje dobře známou URL pro autokonfiguraci:

.. list-table:: OIDC autokonfigurace
   :header-rows: 1

   * - Prostředí
     - Adresa
   * - testovací
     - https://rest-openidconnectapi.caais-test-ext.gov.cz/.well-known/openid-configuration
     
       .. - https://rest-openidconnectapi.caais-test-ext.gov.cz/.well-known/oauth-authorization-server
   * - provozní
     - https://rest-openidconnectapi.caais.gov.cz/.well-known/openid-configuration
     
       .. - https://rest-openidconnectapi.caais.gov.cz/.well-known/oauth-authorization-server

Pokud je uživatel připojen do Centrálního místa služeb (CMS), používá místo domény **gov.cz** doménu **cms2.cz**.

Uvedené JSON soubory autokonfigurace obsahuje seznamy dostupných endpointů, stejně tak výčty podporovaných typů a služeb, proto doporučujeme se s jeho obsahem alespoň zběžně seznámit.

.. _oidc_core: https://openid.net/specs/openid-connect-core-1_0.html
.. _oidc_dicover_conf: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig
