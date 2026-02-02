==============================
Technická specifikace SAML 2.0
==============================

*Tato kapitola obsahuje podrobnou technickou specifikaci pro komunikaci systémů AIS se systémem CAAIS pomocí protokolu SAML 2.0.*

.. _api_saml:autokonfigurace:

SAML 2.0 autokonfigurace
========================

Na následující URL adrese je k dispozici XML s metadaty služby:

.. list-table::
   :header-rows: 1

   * - Prostředí
     - Adresa
   * - testovací NAKIT
     - https://rest-externalsaml2api.caais-test-ext.gov.cz/samlIdpMetadata.xml
   * - provozní
     - `https://rest-externalsaml2api.caais.[doména]/samlIdpMetadata.xml <https://rest-externalsaml2api.caais.gov.cz/samlIdpMetadata.xml>`_

       kde [doména] je **gov.cz** nebo **cms2.cz**.

Jsou v něm obsaženy informace o certifikátech (šifrovacím a podepisovacím), které webová služba používá a dále seznam atributů uživatele, které se vrací v odpovědi webové služby. 

.. list-table:: Popis jednotlivých atributů v XML souboru s metadaty
   :header-rows: 1
   :name: saml_metadata_attrs

   * - Atribut
     - Popis
   * - ``Signature``
     - Podpis XML souboru + certifikát pro ověření platnosti tohoto podpisu.
   * - ``KeyDescriptor use="encryption"``
     - Šifrovací certifikát webové služby zakódován pomocí Base64.
   * - ``KeyDescriptor use="signing"``
     - Podepisovací certifikát webové služby zakódován pomocí Base64.
   * - ``Attribute``
     - Element obsahující informace o atributu uživatele, který se vrací v SAML response. Systém CAAIS vrací pouze takovou sadu atributů, o které je požádán v SAML requestu (automaticky se nevrací kompletní seznam atributů).


.. _api_saml:login_url:

URL pro přihlášení v CAAIS
==========================

Pokud systém AIS zjistí, že uživatel přistupující na stránku AIS není přihlášen, vygeneruje SAML request, zakóduje ho a přesměruje uživatele s tímto požadavkem na přihlašovací stránku CAAIS, která má následující adresu:

.. list-table::
   :header-rows: 1

   * - Prostředí
     - Adresa
   * - testovací NAKIT
     - \https://rest-externalsaml2api.caais-test-ext.gov.cz/samlAuthnRequest?SAMLRequest=zakódovaný_SAML_request&RelayState=vlastní_identifikátor
   * - provozní
     - \https://rest-externalsaml2api.[doména]/samlAuthnRequest?SAMLRequest=zakódovaný_SAML_request&RelayState=vlastní_identifikátor

       kde [doména] je **gov.cz** nebo **cms2.cz**.

Je-li potřeba na straně AIS odlišit více odeslaných požadavků, lze v adrese využít nepovinný ``RelayState`` pro uložení vlastního identifikátoru požadavku. V odpovídající odpovědi ze systému CAAIS se pak tento identifikátor také vrací. Definice struktury SAML request a způsob kódování je uveden v kapitole :ref:`api_saml:request`.

.. _api_saml:response_url:

URL pro příjem SAML response na straně AIS
==========================================

V systému CAAIS je v konfiguraci AIS definována URL, na kterou je po úspěšném ověření uživatel přesměrován. Na tuto URL se předává v CAAIS vygenerovaná a zakódovaná SAML response, ve které je předáván atribut ``SAMLResponse`` a případně také nepovinný atribut ``RelayState`` s identifikátorem uvedeným v požadavku. Na této URL operuje AIS a danou SAML response přijímá.

Základní struktura URL, na které CAAIS zasílá SAML response, je následující:


.. admonition:: URL pro SAML response
   :class: note

   .. code::

     https://adresa_AIS_uložená_v_konfiguraci_AIS_v_CAAIS?SAMLResponse=zakódovaná_SAML_response&RelayState=vlastní_identifikátor_z_požadavku

Definice struktury této SAML response a způsob kódování je uveden v kapitole :ref:`api_saml:response`.

.. _api_saml:response_attrs:

Seznam atributů uživatele (identity) v SAML response
====================================================

CAAIS může vracet v SAML response následující údaje o autentizovaném uživateli.


.. list-table:: Seznam atributů – SAML Response
   :header-rows: 1
   :name: saml_response
   
   * - Atribut
     - Identifikátor atributu
     - Atribut z datového modelu
   * - Příjmení
     - \http://eidas.europa.eu/attributes/naturalperson/CurrentFamilyName
     - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
   * - Jméno
     - \http://eidas.europa.eu/attributes/naturalperson/CurrentGivenName
     - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
   * - Datum narození
     - \http://eidas.europa.eu/attributes/naturalperson/DateOfBirth
     - 
   * - Místo narození
     - \http://eidas.europa.eu/attributes/naturalperson/PlaceOfBirth
     - 
   * - Země narození
     - \http://www.stork.gov.eu/1.0/countryCodeOfBirth
     - 
   * - Pseudonym
     - \http://eidas.europa.eu/attributes/naturalperson/PersonIdentifier
     - "Mapování SeP"." SePBSI" (ServiceMapping.sepBsi) pro daný "Profil"."uživatelské jméno" (Profile.loginName), poznámka – BSI se generuje v CAAIS nové, nemigruje se z JIP/KAAS
   * - Zkratka subjektu
     - LegalEntityShorcut
     - "Subjekt"."zkratka" (Subject.shortcut)
   * - IČO subjektu
     - \http://eidas.europa.eu/attributes/legalperson/LEI
     - "Subjekt"."ič" (Subject.identificationNumber)
   * - Uživatelské jméno
     - Username
     - "Profil"."uživatelské jméno" (Profile.loginName)
   * - Titul před jménem
     - DegreeBefore
     - "Profil"."Fyzická osoba"."titul před" (Profile.PhysicalPerson.degreeBefore)
   * - Titul za jménem
     - DegreeAfter
     - "Profil"."Fyzická osoba"."titul za" (Profile.PhysicalPerson.degreeAfter)
   * - Přístupové role
     - AccessRoles
     - "Profil"."Přístupová role" (Profile.AccessRole)
       pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role, dotahují se přes ně odpovídající přístupové role. Dále se dotahují i delegované přístupové role přes "Vazební profil".

       V seznamu přístupových rolí se vrací pouze role pro daný AIS, do kterého se uživatel autentizuje.

       V atributu bude formát XML v base64, např. takto:

       .. code-block:: xml

          <AccessRoles>
              <AccessRoleCode>editor</AccessRoleCode>
              <AccessRoleCode>spravce</AccessRoleCode>
          </AccessRoles>
   * - Kód přístupové role
     - AccessRoleCode
     - "Přístupová role"."zkratka" (AccessRole.shortcut)
   * - Činnostní role
     - ActivityRoles
     - "Profil"."Činnostní role" (Profile.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

       Pokud má profil přiřazeny Skupiny rolí nebo Business role, dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".

       V atributu bude formát XML v base64, např. takto:
       
       .. code-block:: xml

          <ActivityRoles>
              <Agenda>
                  <AgendaCode>K100</AgendaCode>
                  <ActivityRoleCode>CR1111</ActivityRoleCode>
                  <ActivityRoleCode>CR2222</ActivityRoleCode>
              </Agenda>
          </ActivityRoles>
   * - Kód agendy
     - AgendaCode
     - "Činnostní role"."Agenda"."kód" (ActivityRole.Agenda.code)
   * - Kód činnostní role
     - ActivityRoleCode
     - "Činnostní role"."kód" (ActivityRole.code)
   * - Email
     - \http://www.stork.gov.eu/1.0/eMail
     - "Profil"."email" (Profile.email)
   * - Telefon
     - \http://eidas.europa.eu/attributes/naturalperson/PhoneNumber
     - "Profil"."Telefon" (Profile.PhoneNumber)
     
       Vybere se první telefonní číslo s typem „mobilní“, tedy "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code) = 2. Pokud takové neexistuje, vybere se první telefonní číslo jiného typu. Řazení telefonů je podle databázového ID.
        
       Formát telefonního čísla je podle ITU-E.164 (např. +420777000000).
   * - Název subjektu
     - LegalEntityName
     - "Subjekt"."název" (Subject.name)
   * - Email subjektu
     - LegalEntityEmail
     - "Subjekt"."Kontakt"."Email"."adresa" (Subject.Contact.Email.address) kde "Email"."Typ emailu"."název" (Email.EmailType.name) = "Oficiální"
   * - Typ instituce
     - InstitutionType
     - "Subjekt"."Typ instituce"."kód" (Subject.InstitutionType.code)
   * - Osoba ztotožněna
     - PersonIdentified
     - "Profil"."Fyzická osoba"."osoba evidována v rob" (Profile.PhysicalPerson.personInRob)
   * - Statutární zástupce
     - IsStatutoryRepresentative
     - Atribut z datového modelu: "Profil"."statutární zástupce" (Profile.statutoryRepresentative), příznak (true/false), že je uživatel statutárním zástupcem daného subjektu. 
   * - Datum úmrtí
     - DateOfDeath
     - "Profil"."Fyzická osoba"."datum úmrtí" (Profile.PhysicalPerson.deathDate)
   * - Doklady
     - DocumentIds
     - V CAAIS je pouze 1 doklad
       Doklad (+ atribut Typ)
       DocumentId (+ atribut Type)
       "Profil"."Fyzická osoba"."číslo dokladu" (Profile.PhysicalPerson.documentId)
       a
       "Profil"."Fyzická osoba"."druh dokladu" (Profile.PhysicalPerson.documentType)

       V atributu bude formát XML v base64, např. takto:
       
       .. code-block:: xml

          <DocumentIds>
              <DocumentId Type="ID">111</DocumentId>
              <DocumentId Type="P">222</DocumentId>
          </DocumentIds>
   * - Identifikátor OVM
     - PublicOrganizationIdentifier
     - "Subjekt"."kód ovm v rovm" (Subject.ovmInRovmCode)
   * - Identifikátor SPUÚ
     - AuthorizedPrivateEntityPersonalDataUserIdentifier
     - "Subjekt"."kód spuú" (Subject.spuuCode)
   * - Autorizační token
     - TimeLimitedId
     - Technický atribut pro ukládání tokenů (neuveden v DM)


AIS do SAML requestu uvádí vybranou sadu z těchto atributů, které požaduje vrátit v SAML response. AIS může v SAML request definovat, zda požaduje vrátit atribut jako povinný nebo nepovinný. Pokud požaduje povinný atribut, na který ale nemá oprávnění, systém CAAIS v SAML response vrací chybovou zprávu o neúspěšném přihlášení.

.. _api_saml:request:

Definice SAML request
=====================

Jak bylo uvedeno v kapitole :ref:`api_saml:login_url`, AIS nepřihlášeného uživatele přesměruje na definovanou URL se zakódovaným SAML requestem. Níže je uvedena definice XML struktury pro nezakódovaný SAML request typu SAML2 AuthnRequest:

.. list-table:: Popis jednotlivých elementů – SAML2 AuthnRequest
   :header-rows: 1
   :name: saml_authrequest
   
   * - Atribut
     - Popis
   * - ``AuthnRequest``
     - Element obsahující vlastní atributy SAML requestu.
   * - ``AssertionConsumerServiceURL``
     - Standardně obsahuje URL pro odpověď. CAAIS však tuto hodnotu ignoruje a řídí se návratovou URL definovanou v konfiguraci AIS v CAAIS.
   * - ``Destination``
     - URL přihlašovací stránky CAAIS (viz kapitola :ref:`api_saml:login_url`). Z hodnoty atributu lze ověřit, že request přichází z AIS a je určen pro CAAIS.
   * - ``ID``
     - Jedinečné ID SAML requestu, který si definuje AIS. CAAIS v SAML response vrací stejnou hodnotu v atributu ``InResponseTo``.
   * - ``IssueInstant``
     - Datum a čas vygenerování SAML requestu.
       CAAIS z důvodu bezpečnosti ve chvíli zpracování ignoruje SAML requesty starší než 60 minut.
   * - ``Issuer``
     - Zkratka AIS uvedená v CAAIS
   * - ``Signature``
     - Podpis XML dat requestu + certifikát pro ověření platnosti tohoto podpisu.
   * - ``Extensions``
     - Rozšíření požadavku.
   * - ``SPType``
     - Typ Service Providera (veřejný, privátní). V systému CAAIS se aktuálně hodnota tohoto atributu ignoruje.
   * - ``RequestedAttributes``
     - Seznam povinných/nepovinných údajů uživatele, které AIS požaduje vrátit z CAAIS (viz kapitola :ref:`api_saml:response_attrs`). 
   * - ``AuthnContextClassRef``
     - Požadované LoA (detail viz kapitola :ref:`api_saml:loa`).


S vygenerovaným SAML requestem je nutné provést následující akce, než bude přesměrován:
    
    - komprimace algoritmem Deflate, 
    - zakódování pomocí Base64,
    - URL enkódování – nealfanumerické znaky se nahradí "%" a hexadecimální číslicí.

.. _api_saml:response:

Definice SAML response
======================

Jak bylo uvedeno v kapitole :ref:`api_saml:response_url`, CAAIS přesměruje úspěšně ověřeného uživatele na definovanou URL se zakódovanou SAML response (+ volitelně atribut ``RelayState``). Níže je uvedena definice XML struktury pro nezakódovanou a nezašifrovanou SAML response typu SAML2 Response:

.. list-table:: Popis jednotlivých atributů – element ``Assertion`` před zašifrováním
   :header-rows: 1
   :name: saml_assertion_element

   * - Atribut
     - Popis
   * - ``Issuer``
     - Identifikátor CAAIS-IdP ve funkci Identity Provider.
   * - ``Signature``
     - Podpis XML souboru + certifikát pro ověření platnosti tohoto podpisu.
   * - ``Subject``
     - Základní informace autentizovaného uživatele (např. pseudonym).
   * - ``AttributeStatement``
     - Element se seznamem atributů autentizovaného uživatele (identity), viz tabulka kapitola :ref:`api_saml:response_attrs`.
   * - ``AuthnContextClassRef``
     - Skutečně dosažené LoA (detail viz kapitola :ref:`api_saml:loa`).

     
S vygenerovanou SAML response je nutné provést následující akce, než bude vložena na definovanou URL:

    - komprimace algoritmem Deflate, 
    - zakódování pomocí Base64,
    - URL enkódování – nealfanumerické znaky se nahradí "%" a hexadecimální číslicí.

Po zašifrování šifrovacím certifikátem je element ``EncryptedAssertion`` určen pro následné podepsání podepisovacím certifikátem (oba certifikáty uloženy v konfiguraci AIS v CAAIS). V elementu ``EncryptedAssertion`` se nachází zašifrovaná data (uložena v elementu ``CipherData``) + další atributy týkající se šifrování. 


.. admonition:: Příklad - pro jednoduchost uveden začátek URL bez parametru ``RelayState``
   :class: note

   .. code::

     https://adresa_AIS?SAMLResponse=7bvZjuRGki58f55CqLkMqLlvhZYOuAS3CJLBncGbA%2B77vvO1ziP8L%2FYzq1RqSa2ekXoa…

     
.. _api_saml:loa:
     
Úroveň záruk (Level of Assurance)
=================================

V systému CAAIS je přiřazení úrovní záruk definováno pouze pro certifikované autentizační systémy (IdP) – např. NIA. Pokud se uživatel autentizuje pomocí NIA, vrací se v odpovědi přihlašovací metody do AIS taková úroveň LoA, kterou NIA předal.
Autentizuje-li se uživatel pomocí vnitřního systému CAAIS-IdP, vrací se v odpovědi vždy nejnižší úroveň LoA, podle toho, která byla použita v SAML (viz tabulka níže):

    - http://eidas.europa.eu/NotNotified/LoA/low
    - http://eidas.europa.eu/LoA/NotNotified/low (podle toho která hodnota byla použita v requestu).

Úroveň LoA znamená míru důvěryhodnosti, s jakou se uživatel autentizoval. Nejčastěji se používají úrovně nízká, značná a vysoká. V systému CAAIS se pracuje s těmito LoA:

.. list-table:: Hodnoty LoA
   :header-rows: 1

   * - LoA
     - Standardizovaný identifikátor
   * - nízká
     -
        - http://eidas.europa.eu/NotNotified/LoA/low
        - http://eidas.europa.eu/LoA/low
        - http://eidas.europa.eu/LoA/NotNotified/low (hodnota někdy nesprávně používána zahraničními systémy, CAAIS ji také podporuje)
   * - značná
     -
        - http://eidas.europa.eu/NotNotified/LoA/substantial
        - http://eidas.europa.eu/LoA/substantial
   * - vysoká
     -
        - http://eidas.europa.eu/NotNotified/LoA/high
        - http://eidas.europa.eu/LoA/high


Požadované LoA se uvádí v SAML requestu v atributu ``AuthnContextClassRef``. V atributu ``Comparison`` (hodnoty ``exact``, ``minimum``, ``maximum`` nebo ``better``) se pak definuje způsob porovnávání požadované LoA a dostupné LoA. Pro SAML requesty odesílané do systému CAAIS se doporučuje hodnota ``minimum``.

V SAML response se ve stejném atributu ``AuthnContextClassRef`` pak vyplní skutečné LoA podle způsobu autentizace uživatele.
