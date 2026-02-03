.. _changelog:

.. role:: ticket

=============
Verze a změny
=============

*Stručně popsané syntaktické či sémantické změny a opravy API od počátku roku 2026 – verze 2.17.*

verze 2.18 (2026-02-03)
-----------------------

- Přidej persistentní atribut UUID pro subjekt. Předávej jej protokoly OIDC a SAML 2.0. :ticket:`closes #198`
- Vynuť předávání atributů v SAML 2.0 response bez explicitního požadavku jen na základě konfigurace AIS. :ticket:`closes #276`
- Oprav API JIP/KAAS editačních webových služeb:
  
  - Vracej v ``CreateUserResponse`` vždy atribut ``object-id``. :ticket:`fixes #310`
  - Změň časová razítka v odpovědích kvůli kompatibilitě s JIP/KAAS na unix timestamp v sekundách (původně milisekundy). :ticket:`fixes #321`
  - Oprav xmlns v ``GetVersionResponse`` pro edit/3. :ticket:`fixes #322`
  - Oprav stav zrušeno v ``GetOrganizationResponse``. :ticket:`fixes #326`
  - Oprav zpracování explicitních namespace. :ticket:`fixes #319`
  - Změn výchozí typ certifikátů v CAAIS IdP na komerční (původně kvalifikovaný). :ticket:`fixes #329`

verze 2.17 (2026-01-21)
-----------------------

- Aktualizuj API JIP/KAAS editačních webových služeb:

  - Vracej v ``getUserResponse`` boolean element ``isLocalAdmin``.
