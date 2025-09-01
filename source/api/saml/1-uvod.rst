Úvod
====

Účelem tohoto dokumentu je popsat technické detaily uživatelské autentizace do agendových informačních systémů (AIS), které jsou registrovány v systému CAAIS. Uživatel používá přihlašovací údaje do systému CAAIS-IdP (modul interního IdP CAAIS), který zde plní funkci autentizačního informačního systému dle § 56a zákona č. 111/2009 Sb., o základních registrech.

Komunikace a předávání údajů o uživateli je prováděna pomocí protokolu SAML 2.0, který se využívá pro výměnu autentizačních a autorizačních dat. Prostřednictvím SAML 2.0 protokolu se v rámci přesměrovávání uživatele mezi AIS a CAAIS předává definovaná sada atributů (viz kapitola :ref:`api_saml:response_attrs`), která je podmnožinou všech atributů, které jsou o uživateli (identitě) v systému CAAIS-IdP vedeny. Při autentizaci SAML protokolem se ani nevolají žádné další webové služby CAAIS (např. editační) pro získání ostatních atributů.
