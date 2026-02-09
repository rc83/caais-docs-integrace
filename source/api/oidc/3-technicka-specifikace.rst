==========================
Technická specifikace OIDC
==========================

*Tato kapitola obsahuje podrobnou technickou specifikaci pro komunikaci systémů AIS se systémem CAAIS pomocí protokolu OIDC.*

OIDC autokonfigurace
====================

OIDC definuje dobře známou URL pro dokument s `konfigurací OpenID Providera <oidc_dicover_conf_>`_. Dokument je ve formátu JSON a obsahuje seznamy dostupných endpointů, výčty podporovaných typů a služeb a další podrobnosti. Pro CAAIS je dostupný na adresách níže. 

.. _oidc_dicover_conf: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig

.. list-table:: OIDC autokonfigurace
   :header-rows: 1

   * - Prostředí
     - Adresa
   * - testovací
     - https://rest-openidconnectapi.caais-test-ext.gov.cz/.well-known/openid-configuration
   * - provozní
     - https://rest-openidconnectapi.caais.gov.cz/.well-known/openid-configuration

Pokud jste připojeni do Centrálního místa služeb (CMS), použijete místo domény **gov.cz** doménu **cms2.cz**.

Podpisové klíče
---------------

CAAIS podepisuje vydávané JWT (JSON Web Token). Obdržený token je nutné ověřit pomocí veřejného klíče z JSON Web Key Set (JWKS), která je publikovaná na adresách níže.

.. list-table::  Endpointy pro JSON Web Key Set (JWKS)
   :header-rows: 1

   * - Prostředí
     - Adresa
   * - testovací
     - https://rest-openidconnectapi.caais-test-ext.gov.cz/oauth2/jwks
   * - provozní
     - https://rest-openidconnectapi.caais.gov.cz/oauth2/jwks

Pokud jste připojeni do Centrálního místa služeb (CMS), použijete místo domény **gov.cz** doménu **cms2.cz**.
       
Uvedenou URL lze též získat přímo ze základní konfigurace. Volitelný ``kid`` parametr (Key ID; :rfc:`7517#section-4.5`) není v JWKS využíván.


Popis autorizačního endpointu pro přihlášení uživatele
======================================================

Pokud na AIS přistoupí nepřihlášený uživatel, provede AIS přesměrování na *autorizační endpoint* CAAISu.

Tabulka níže obsahuje seznam dostupných parametrů, které se posílají na *autorizační endpoint* CAAIS při žádosti o přihlášení uživatele. Některé z nich jsou povinné. Parametry je možné předat jak HTTP metodou GET (jako součást query string URL), tak POST.


.. list-table::  Seznam parametrů na *autorizační endpoint*
   :header-rows: 1
   :name: oidc_query_params

   * - Parametr
     - Povinný
     - Popis
   * - ``client_id``
     - ano
     - Identifikátor Relying Party (AIS). V hodnotě se posílá zkratka AIS, jak je zadána v konfiguraci AIS v CAAIS.
   * - ``redirect_uri``
     - ano
     - Sem je po úspěšném přihlášení v CAAIS uživatel přesměrován. Musí odpovídat některé z hodnot, které jsou u AIS nakonfigurovány jako návratové URL.
   * - ``scope``
     - ano
     - Seznam oprávnění, které Relying Party vyžaduje od Resource Ownera – seznam hodnot oddělených mezerou. Viz kapitola :ref:`oidc:atributy`.
   * - ``response_type``
     - ano
     - Typ odpovědi po úspěšném přihlášení uživatele. Musí obsahovat hodnotu ``code``.
   * - ``code_challenge``
     - ne
     - Chrání před zneužitím autorizačního kódu. Původně určená pro PKCE flow (:rfc:`7636`), ale pro zvýšení bezpečnosti doporučujeme používat vždy. Následná žádost jdoucí na *token endpoint* musí obsahovat odpovídající ``code_verifier``. Hodnota ``code_challenge`` je base64url kódovaná SHA256 hash hodnoty ``code_verifier``.
   * - ``nonce``
     - ne
     - Parametr, užívaný k zabránění tzv. „replay“ útokům. Obsahuje náhodně vygenerovanou hodnotu. Pokud ji AIS pošle, CAAIS přidá „nonce“ claim do identity tokenu. AIS poté musí ověřit, že obdržená hodnota v daném claimu odpovídá odeslané hodnotě. Doporučujeme používat pro zvýšení bezpečnosti.
   * - ``state``
     - ne
     - Po úspěšném přihlášení uživatele provede CAAIS přesměrování na AIS a beze změny pošle tuto hodnotu v parametrech. Toto má dvoje využití, jež je možné kombinovat:
       
       I. AIS si přes proces přihlašování drží stav (například variabilní parametry URL, kam je uživatel po přihlášení přesměrován). Citlivé údaje by měly být zašifrovány.
       
       II. Ochrana před Cross-Site Request Forgery (CSRF) útoky. Parametr obsahuje náhodnou hodnotu. AIS následně ověřuje, že obdržená hodnota odpovídá té, kterou odeslal při přesměrování uživatele na CAAIS.

          
     
.. admonition:: Povinné mTLS
   :class: warning
   
   Parametr ``client_secret`` se nepoužívá. Místo toho ověření AIS spoléhá na mTLS, jak indikuje hodnota ``tls_client_auth`` v seznamu ``token_endpoint_auth_methods_supported`` v základní konfiguraci. Ověřuje ověřuje se prostá shoda klientského certifikátu vůči certifikátu uloženému v konfiguraci AIS (:rfc:`8705#name-pki-mutual-tls-method`).

   
.. admonition:: URL pro žádost o přihlášení
   :class: note

   .. code::

      https://rest-openidconnectapi.caais-test-ext.gov.cz/oauth2/authorize
      ?client_id=my_ais_shortcut
      &redirect_uri=https%3A%2F%2Fexample.org%2Flogin
      &scope=openid%20profile
      &response_type=code
      &code_challenge=aMmkIhFlicd0kYXQyGjE9u21JCM40Fu3c6qsfMqkssc
      &code_challenge_method=S256
      &nonce=my_nonce
      &state=my_state


Rozhraní stránky AIS pro návrat po úspěšném přihlášení
------------------------------------------------------

Po úspěšném ověření CAAIS přesměruje uživatele zpátky na AIS URL, která byla poslána v parametru ``redirect_uri``. Do adresy doplní parametr ``code`` obsahující vygenerovaný kód, který AIS následně použije pro získání *access tokenu* a *identity tokenu*. Pokud AIS předal parametr ``state``, CAAIS vrátí tento parametr s nezměněnou hodnotou.
Základní struktura URL, na kterou CAAIS přesměruje uživatele po přihlášení:

.. admonition:: URL pro přesměrování po přihlášení
   :class: note

   .. code::

      https://example.org/login?code=hodnota&state=my_state


.. admonition:: HTTP 400 Bad Request
   :class: warning
   
   Pokud pokus o přihlášení místo přesměrování končí chybou HTTP 400 Bad Request, je nejčastější příčina v parametrech poskytnutých v iniciální URL pro přihlášení. Může se jednat o chybějící povinné parametry, neplatné či neznámé hodnoty parametrů či nesoulad hodnot parametrů s konfigurací AIS v CAAIS – například použitá ``redirect_uri`` není v konfiguraci AIS v CAAIS uvedená mezi povolenými adresami pro přesměrování.


.. _oidc:atributy:

Seznam atributů uživatele (profilu) v identity tokenu
=====================================================

CAAIS může vracet v *identity tokenu* uživatele následující údaje o autentizovaném uživateli, respektive jeho profilu.
AIS definuje při žádosti o přihlášení parametr ``scope``, skrze který může specifikovat údaje, které chce o uživateli získat. Jednotlivé hodnoty v parametru ``scope`` jsou odděleny mezerou. Parametr ``scope`` musí vždy obsahovat hodnotu ``openid``.

.. list-table::  Seznam atributů v identity tokenu
   :header-rows: 1

   * - Atribut
     - Claim v ID tokenu
     - Potřebný scope
     - Atribut z datového modelu
   * - Příjmení
     - family_name
     - profile
     - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
   * - Jméno
     - given_name
     - profile
     - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
   * - Datum narození
     - birthdate
     - birthdate
     -
   * - Místo narození
     - birthplace
     - birthplace
     -
   * - Země narození
     - country_of_birth
     - country_of_birth
     -
   * - Pseudonym
     - sub
     - oidc
     - "Mapování SeP"." SePBSI" (ServiceMapping.sepBsi) pro daný "Profil"."uživatelské jméno" (Profile.loginName), poznámka – BSI se generuje v CAAIS nové, nemigruje se z JIP/KAAS
   * - Přístupové role
     - access_roles
     - profile
     - Seznam přístupových rolí do AIS přiřazených uživateli.

       "Profil"."Přístupová role" (Profile.AccessRole)
       pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role, dotahují se přes ně odpovídající přístupové role. Dále se dotahují i delegované přístupové role přes "Vazební profil".

       V seznamu přístupových rolí se vrací pouze role pro daný AIS, do kterého se uživatel autentizuje.
   * - role
     - role
     - profile
     - Kód přístupové role.

       "Přístupová role"."zkratka" (AccessRole.shortcut)
   * - Činnostní role
     - activity_roles
     - profile
     - Seznam činnostních rolí přiřazených uživateli.

       "Profil"."Činnostní role" (Profile.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".
   * - Kód agendy
     - agenda_code
     - profile
     - Kód agendy činnostní role.

       "Činnostní role"."Agenda"."kód" (ActivityRole.Agenda.code)
   * - Kód činnostní role
     - activity_role_code
     - profile
     - Kód činnostní role.

       "Činnostní role"."kód" (ActivityRole.code)
   * - Zkratka subjektu
     - legal_entity_shorcut
     - subject
     - "Subjekt"."zkratka" (Subject.shortcut)
   * - IČO subjektu
     - lei
     - subject
     - "Subjekt"."ič" (Subject.identificationNumber)
   * - Uživatelské jméno
     - username
     - profile
     - "Profil"."uživatelské jméno" (Profile.loginName)
   * - Titul před jménem
     - degree_before
     - profile
     - "Profil"."Fyzická osoba"."titul před" (Profile.PhysicalPerson.degreeBefore)
   * - Titul za jménem
     - degree_after
     - profile
     - "Profil"."Fyzická osoba"."titul za" (Profile.PhysicalPerson.degreeAfter)
   * - Přístupové role
     - access_roles
     - role
     - "Profil"."Přístupová role" (Profile.AccessRole)
       pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role, dotahují se přes ně odpovídající přístupové role. Dále se dotahují i delegované přístupové role přes "Vazební profil".

       V seznamu přístupových rolí se vrací pouze role pro daný AIS, do kterého se uživatel autentizuje.

       V atributu bude formát JSON, např. takto:

        .. code-block:: json

           "access_roles": [
             {
               "access_role_code": "editor"
             },
             {
               "access_role_code": "spravce"
             }
           ]
   * - Kód přístupové role
     - access_role_code
     - role
     - "Přístupová role"."zkratka" (AccessRole.shortcut)
   * - Činnostní role
     - activity_roles
     - role
     - "Profil"."Činnostní role" (Profile.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role, dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".

       V atributu bude formát JSON, např. takto:

        .. code-block:: json

           {
             "activity_roles": [
               {
                 "agenda_code": "K100",
                 "activity_role_code": [
                   "CR1111",
                   "CR2222"
                 ]
               },
               {
                 "agenda_code": "K101",
                 "activity_role_code": [
                   "CR3333",
                   "CR4444"
                 ]
               }
             ]
           }
   * - Kód agendy
     - agenda_code
     - role
     - "Činnostní role"."Agenda"."kód" (ActivityRole.Agenda.code)
   * - Kód činnostní role
     - activity_role_code
     - role
     - "Činnostní role"."kód" (ActivityRole.code)
   * - Email
     - email
     - contact
     - "Profil"."email" (Profile.email)
   * - Telefon
     - phone_number
     - contact
     - "Profil"."Telefon" (Profile.PhoneNumber) 
     
       Vybere se první telefonní číslo s typem „mobilní“, tedy "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code) = 2. Pokud takové neexistuje, vybere se první telefonní číslo jiného typu. Řazení telefonů je podle databázového ID.
       
       Formát telefonního čísla odpovídá ITU-E.164 (např. +420777000000).
   * - Název subjektu
     - legal_entity_name
     - subject
     - "Subjekt"."název" (Subject.name)
   * - Email subjektu
     - legal_entity_email
     - subject
     - "Subjekt"."Kontakt"."Email"."adresa" (Subject.Contact.Email.address) kde "Email"."Typ emailu"."název" (Email.EmailType.name) = "Oficiální"
   * - Typ instituce
     - institution_type
     - subject
     - "Subjekt"."Typ instituce"."kód" (Subject.InstitutionType.code)
   * - Osoba ztotožněna
     - person_identified
     - profile
     - "Profil"."Fyzická osoba"."osoba evidována v rob" (Profile.PhysicalPerson.personInRob)
   * - Statutární zástupce
     - is_statutory_representative
     - profile
     - "Profil"."statutární zástupce" (Profile.statutoryRepresentative), příznak (true/false), že je uživatel statutárním zástupcem daného subjektu.
   * - Datum úmrtí
     - date_of_death
     - deathdate
     - "Profil"."Fyzická osoba"."datum úmrtí" (Profile.PhysicalPerson.deathDate)
   * - Doklady
     - document_ids
     - document
     - V CAAIS je pouze 1 doklad
   * - Doklad (+ atribut Typ)
     - document_id (+ atribut type)
     - document
     - "Profil"."Fyzická osoba"."číslo dokladu" (Profile.PhysicalPerson.documentId)
       a
       "Profil"."Fyzická osoba"."druh dokladu" (Profile.PhysicalPerson.documentType)

       V atributu bude formát JSON, např. takto:
       
        .. code-block:: json

           {
             "document_ids": [
               {
                 "type": "Občanský průkaz",
                 "document_id": "A1234"
               },
               {
                 "type": "Pas",
                 "document_id": "123456789"
               }
             ]
           }
   * - Identifikátor OVM
     - | public\_organization
       | \_identifier
     - subject
     - "Subjekt"."kód ovm v rovm" (Subject.ovmInRovmCode)
   * - Identifikátor SPUÚ
     - | authorized\_private
       | \_entity\_personal
       | \_data\_user\_identifier
     - subject
     - "Subjekt"."kód spuú" (Subject.spuuCode)
   * - UUID
     - legal_entity_unique_identifier
     - subject
     - "Subjekt"."unikátní identifikátor" (Subject.uniqueIdentifier)
   * - Autorizační token
     - time_limited_id
     - role
     - Technický atribut pro ukládání tokenů (neuveden v DM)


.. admonition:: URL pro žádost o přihlášení
   :class: note

   .. code::

     https://rest-openidconnectapi.caais-test-ext.gov.cz/oauth2/authorize
     ?client_id=my_ais_shortcut
     &redirect_uri=https%3A%2F%2Fexample.org%2Flogin
     &scope=openid%20profile%20subject%20contact%20document
     &response_type=code
     &code_challenge=0Aw3qcaENBz7RM378ZdZZ0UXRvcqpGJSz6JnymyBeVI
     &nonce=my_nonce
     &state=my_state


Získání tokenů
==============

Ve chvíli, kdy má AIS k dispozici ``code`` získaný po přihlášení uživatele, musí jej přeposlat na *token endpoint* CAAIS, aby jej vyměnil za *access token* a *identity token*. Žádost o tokeny musí proběhnout pomocí HTTP POST dotazu uvnitř mTLS spojení – AIS se musí autentizovat klientským certifikátem, který má registrován ve své konfiguraci v CAAIS. AIS pošle v dotazu následující parametry:

  - ``grant_type`` s hodnotou ``authorization_code``;
  - ``code`` s obdrženou hodnotou;
  - ``redirect_uri``, která byla použita při přihlášení uživatele;
  - ``code_verifier``, byl-li použit ``code_challenge``.

Struktura dotazu vypadá následovně:

.. admonition:: Příklad dotazu
   :class: note

   .. code:: http

      POST http://cert-openidconnectapi.caais-test-ext.gov.cz/oauth2/token HTTP/1.1
      Content-Type: application/x-www-form-urlencoded

      grant_type=authorization_code&code=hodnota&client_id=my_ais_shortcut&redirect_uri=https%3A%2F%2Fexample.org%2Flogin


.. admonition:: Ukázka dotazu
   :class: note

   .. code:: http

    POST https://cert-openidconnectapi.caais-test-ext.gov.cz/oauth2/token HTTP/1.1
    Host: cert-openidconnectapi.caais-test-ext.gov.cz
    Accept: */*
    Accept-Encoding: gzip, deflate, br, zstd
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 284
    Connection: Keep-Alive
    User-Agent: python-requests/2.32.4

    grant_type=authorization_code&code=i7JgcKjzWjxOwMnKg_9W1p1sXTmkz3Wr-6o-GuIeGjrSyKuD3MuQXT4h5uhtwLOClhAzN5qMQOAsTWBKOVALtzr5xndzQF5bXIxfTk_cy4369bcoJN4FNDw-9Bm9zfD2&client_id=MY_AIS&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foidc-login&scope=openid+profile&code_verifier=my_challenge

CAAIS ověří obdržené údaje. Pokud jsou správné, odešle v odpovědi access token a identity token. Odpověď pak může vypadat následovně:

.. admonition:: Příklad odpovědi
   :class: note

   .. code:: json

        {
          "access_token": "[zakódovaný access token]",
          "refresh_token": "[zakódovaný refresh token]",
          "scope": "openid profile",
          "id_token": "[zakódovaný identity token]",
          "token_type": "Bearer",
          "expires_in": 299
        }


.. admonition:: Ukázka odpovědi
   :class: note

   .. code:: json

      {
        "access_token":"eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxNmIzMzY3MC1hODE2LTRjMWEtODcxMi1kOTllOWZmODVmZWMiLCJhdWQiOiJNWV9BSVMiLCJuYmYiOjE3NTU4NzAyNjQsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiXSwiaXNzIjoiaHR0cHM6Ly9yZXN0LW9wZW5pZGNvbm5lY3RhcGkuY2FhaXMtdGVzdC1leHQuZ292LmN6LyIsImV4cCI6MTc1NTg3MDU2NCwiaWF0IjoxNzU1ODcwMjY0LCJqdGkiOiJjYzk3N2JlOS0zYzI5LTQ3NTgtYjlkMi00MDRjNzc0ZTEzZjgiLCJjbGllbnRfY2VydF9zaGEyNTYiOiJtall5RGszLTgycEtFSHpPd3dxVlVEOGR6ZHppTndEaFNPZkcwZHBYLXUwIn0.Yn3_aJovn054PrDERhKQN7uHfrf0MEUfa12s2U4Z3H4lYF-TtS4FzPh27tmZ3wlaXSLoial1KkJhuA6wRmdk-cSSKVsbTCOG3vSnQJVaIS3yg5lRI2EmAUdvhWGSuOUYywV-U69_p3RY7H5yzleDTUvYbgnSIlMY5UJCwuHok0_cxAkOMhkAtMR_hsFOYt5fItXI3oMCa1-C9EnC8ZwOEGxv5ALvdItUl1IRiu6C4nYDpJEmPEgPx7yxvuCec_48avAQ91l-SBrGIAQ-TYYMSBkviyIQ4cPy98BDXlDS8sm0RNV1j-60nJnqkLQGOxXvIPLiHFOBhgfcmGY7ywFU5w",
        "refresh_token":"3JLQZ7I9vpUGvPdIZsO7ys3Uw10H8DRfhvFWc_7Q6PaILveTYS8t1FBT7seAJ07pkv7iyyBnMLiZMzILiVF0_8aNuGzIQB52xAfySmlPIJSXaLRre39mbr8V5ZPn27uf",
        "scope":"openid profile",
        "id_token":"eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxNmIzMzY3MC1hODE2LTRjMWEtODcxMi1kOTllOWZmODVmZWMiLCJwZXJzb25faWRlbnRpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vcmVzdC1vcGVuaWRjb25uZWN0YXBpLmNhYWlzLXRlc3QtZXh0Lmdvdi5jei8iLCJpc19zdGF0dXRvcnlfcmVwcmVzZW50YXRpdmUiOmZhbHNlLCJnaXZlbl9uYW1lIjoiSHVtcGhyZXkiLCJub25jZSI6Im15X25vbmNlIiwic2lkIjoiZU1peHVPdlhXYnQ2eHFaUC1GRW9BbVVJb1JjMzNHV3A4OTR4azBCNjBFdyIsImRlZ3JlZV9iZWZvcmUiOiJTaXIiLCJhdWQiOiJNWV9BSVMiLCJhenAiOiJNWV9BSVMiLCJhdXRoX3RpbWUiOjE3NTU4Njk3MDgsImV4cCI6MTc1NTg3MjA2NCwiaWF0IjoxNzU1ODcwMjY0LCJkZWdyZWVfYWZ0ZXIiOiIiLCJmYW1pbHlfbmFtZSI6IkFwcGxlYnkiLCJqdGkiOiJjOTU1ZDExOS0yOTI3LTQ1ZGMtYTZkZC02OGVlN2Y5YTBmMzEiLCJ1c2VybmFtZSI6Imh1bXBocmV5X2FwcGxlYnkifQ.WLf7bEsMYkzfqQRSCTjoJ12H0rP1R0XeORdt6Wog6rTqnE7syC6_Qylc1k5jPQkvVK88FIfa8hs2kcQ8IQxvlrml3k816wtQGTnahxdcr0s3teyIUxJ36GDz3cEWhY8db7nrBMKmts4BWJeTyyrFv9hkEH5JDBlEQ71JNELZbCBPUYKSBGWIyAKUjOpe8jAfcgpq6vP009fJzST1a2sQ8yJXJ4Uq_JMwvMgJxGkBkVY_Mm8Z9jAHB4TRRppTLQUgCCqZ0B84sFtieMimteQnpbaKPaf_frTXGDjFo-jqp8oB4GErWSMzplATepTbE9wqN5Ebwu4cmYRym6gqnjnwzQ",
        "token_type":"Bearer",
        "expires_in":299
      }

.. admonition:: Ukázka dekódovaného obsahu access tokenu
   :class: note

   .. code:: json

      {
        "aud":"MY_AIS",
        "client_cert_sha256":"mjYyDk3-82pKEHzOwwqVUD8dzdziNwDhSOfG0dpX-u0",
        "exp":1755870564,
        "iat":1755870264,
        "iss":"https://rest-openidconnectapi.caais-test-ext.gov.cz/",
        "jti":"cc977be9-3c29-4758-b9d2-404c774e13f8",
        "nbf":1755870264,
        "scope":["openid","profile"],
        "sub":"16b33670-a816-4c1a-8712-d99e9ff85fec"
      }


.. admonition:: Ukázka dekódovaného obsahu identity tokenu
   :class: note

   .. code:: json

      {
        "aud":"MY_AIS",
        "auth_time":1755869708,
        "azp":"MY_AIS",
        "degree_after":"",
        "degree_before":"Sir",
        "exp":1755872064,
        "family_name":"Appleby",
        "given_name":"Humphrey",
        "iat":1755870264,
        "is_statutory_representative":false,
        "iss":"https://rest-openidconnectapi.caais-test-ext.gov.cz/",
        "jti":"c955d119-2927-45dc-a6dd-68ee7f9a0f31",
        "nonce":"my_nonce",
        "person_identified":false,
        "sid":"eMixuOvXWbt6xqZP-FEoAmUIoRc33GWp894xk0B60Ew",
        "sub":"16b33670-a816-4c1a-8712-d99e9ff85fec",
        "username":"humphrey_appleby"
      }



Popis endpointu pro odhlášení uživatele
=======================================

Pokud AIS odhlásí přihlášeného uživatele (ukončí jeho sezení v AIS), přesměruje následně uživatele na endpoint CAAIS pro odhlášení uživatele v CAAIS.


Tabulka níže obsahuje seznam dostupných query parametrů, které se posílají na CAAIS při žádosti o odhlášení uživatele. Některé z nich jsou povinné. Parametry je možné předat jak HTTP metodou GET (jako součást query string URL), tak POST. Stejně jako při přihlášení je nutné mTLS.

.. list-table::  Seznam query parametrů
   :header-rows: 1
   :name: oidc_logout_query_params

   * - Parametr
     - Povinný
     - Popis
   * - ``client_id``
     - ano
     - Identifikátor Relying Party (AIS), v hodnotě se bude posílat zkratka pro AIS.
   * - ``post_logout_redirect_uri``
     - ano
     - Sem je po úspěšném odhlášení uživatel přesměrován. Musí odpovídat hodnotě, která je u AIS nakonfigurovaná jako návratová URL pro odhlášení.
   * - ``id_token_hint``
     - ano
     - ID Token, který AIS obdržel od CAAIS při přihlášení uživatele. Slouží k identifikaci sezení, jenž se ukončuje.
   * - ``state``
     - ne
     - Po odhlášení uživatele provede CAAIS přesměrování na AIS a beze změny pošle tuto hodnotu v parametrech. Toto má dvoje využití, jež je možné kombinovat:
       
       I. AIS si přes proces odhlašování drží stav (například variabilní parametry URL, kam je uživatel po odhlášení přesměrován). Citlivé údaje by měly být zašifrovány.
       
       II. Ochrana před Cross-Site Request Forgery (CSRF) útoky. Parametr obsahuje náhodnou hodnotu. AIS následně ověřuje, že obdržená hodnota odpovídá té, kterou odeslal při přesměrování uživatele na CAAIS.

Základní struktura URL použitá při žádosti o odhlášení:

.. admonition:: URL pro žádosti o odhlášení
   :class: note

   .. code::

     https://rest-openidconnectapi.caais-test-ext.gov.cz/oauth2/end_session
     ?client_id=my_ais_shortcut
     &post_logout_redirect_uri=https%3A%2F%2Fexample.org%2Flogout
     &id_token_hint=jwt_id_token
     &state=my_state

Po přesměrování uživatele CAAIS nabídne uživateli ukončení single sign-on sezení (odhlášení z CAAIS). Bez ohledu, zda je signle sign-on sezení ukončeno, přesměruje CAAIS uživatele zpět do AIS na hodnotu předanou v ``post_logout_redirect_uri``. Pokud AIS předal parametr ``state``, CAAIS vrátí tento parametr s nezměněnou hodnotou.

.. admonition:: URL pro přesměrování po odhlášení
   :class: note

   .. code::

      https://example.org/logout?state=my_state

.. admonition:: Ukázka dotazu
   :class: note

   .. code:: http

    POST https://cert-openidconnectapi.caais-test-ext.gov.cz/oauth2/end_session HTTP/1.1
    Host: cert-openidconnectapi.caais-test-ext.gov.cz
    Accept: */*
    Accept-Encoding: gzip, deflate, br, zstd
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 1168
    Connection: Keep-Alive
    User-Agent: python-requests/2.32.4
    
    client_id=MY_AIS&post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foidc-logout&state=54ouD8wzw8NXrRYOlmGuHP-7jWbnyPUTxQD_rOi9Gpk&id_token_hint=eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxNmIzMzY3MC1hODE2LTRjMWEtODcxMi1kOTllOWZmODVmZWMiLCJwZXJzb25faWRlbnRpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vcmVzdC1vcGVuaWRjb25uZWN0YXBpLmNhYWlzLXRlc3QtZXh0Lmdvdi5jei8iLCJpc19zdGF0dXRvcnlfcmVwcmVzZW50YXRpdmUiOmZhbHNlLCJnaXZlbl9uYW1lIjoiSHVtcGhyZXkiLCJub25jZSI6Im15X25vbmNlIiwic2lkIjoiZU1peHVPdlhXYnQ2eHFaUC1GRW9BbVVJb1JjMzNHV3A4OTR4azBCNjBFdyIsImRlZ3JlZV9iZWZvcmUiOiJTaXIiLCJhdWQiOiJNWV9BSVMiLCJhenAiOiJNWV9BSVMiLCJhdXRoX3RpbWUiOjE3NTU4Njk3MDgsImV4cCI6MTc1NTg3MjA2NCwiaWF0IjoxNzU1ODcwMjY0LCJkZWdyZWVfYWZ0ZXIiOiIiLCJmYW1pbHlfbmFtZSI6IkFwcGxlYnkiLCJqdGkiOiJjOTU1ZDExOS0yOTI3LTQ1ZGMtYTZkZC02OGVlN2Y5YTBmMzEiLCJ1c2VybmFtZSI6Imh1bXBocmV5X2FwcGxlYnkifQ.WLf7bEsMYkzfqQRSCTjoJ12H0rP1R0XeORdt6Wog6rTqnE7syC6_Qylc1k5jPQkvVK88FIfa8hs2kcQ8IQxvlrml3k816wtQGTnahxdcr0s3teyIUxJ36GDz3cEWhY8db7nrBMKmts4BWJeTyyrFv9hkEH5JDBlEQ71JNELZbCBPUYKSBGWIyAKUjOpe8jAfcgpq6vP009fJzST1a2sQ8yJXJ4Uq_JMwvMgJxGkBkVY_Mm8Z9jAHB4TRRppTLQUgCCqZ0B84sFtieMimteQnpbaKPaf_frTXGDjFo-jqp8oB4GErWSMzplATepTbE9wqN5Ebwu4cmYRym6gqnjnwzQ
