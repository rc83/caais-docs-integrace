.. _api_jip:techspec:

Technická specifikace klasické autentizace
==========================================

.. include:: deprecation-warning.inc.rst

Verze JIP/KAAS legacy API
-------------------------

JIP/KAAS legacy API využívá SOAP protokol verze 1.1. CAAIS k udržení maximální kompatibility s JIP/KAAS podporuje několik verzí jeho API.

.. _api_jip:verze:
.. list-table:: Verze JIP/KAAS legacy API
   :header-rows: 1

   * - Veze
     - WSDL
     - XMLNS
   * - 2.1
     - :download:`GetCredential_v2_1.wsdl <_static/wsdl/GetCredential_v2_1.wsdl>`
     - http\://agw-as.cz/ats-ws/atsSzr/v2_1
   * - 3.4
     - :download:`GetCredential_v3_4.wsdl <_static/wsdl/GetCredential_v3_4.wsdl>`
     - http\://agw-as.cz/ats-ws/atsSzr/v3_4
   * - 4.1
     - :download:`GetCredential_v4_1.wsdl <_static/wsdl/GetCredential_v4_1.wsdl>`
     - http\://agw-as.cz/ats-ws/atsSzr/v4_1
   * - 4.2
     - :download:`GetCredential_v4_2.wsdl <_static/wsdl/GetCredential_v4_2.wsdl>`
     - http\://agw-as.cz/ats-ws/atsSzr/v4_2
     
Ve WSDL souborech jsou vždy uvedeny URL endpointu pro produkční prostředí CAAIS. Pokud je potřeba použít jiné prostředí, je nutné ručně URL upravit.

API ve všech verzích implementuje právě dvě metody ``heartBeat`` a ``authConfirmation``, jak je popsáno ve WSDL souborech. API se liší jmenným prostorem XML, jinak není ve volání metod mezi jednotlivými verzemi rozdíl, pouze se zvětšuje množina údajů vracená v odpovědi ``authConfirmation``, více :ref:`api_jip:atributy`.

verze 2.1: 
  Oproti předchozím verzím byla přidána metoda pro ověření dostupnosti WS a maximální délka atributu ``Username`` byla zvýšena na 50 znaků.
verze 3.4: 
  WS navíc oproti verzi 2.1 vrací více údajů o uživateli a jeho subjektu (viz :ref:`api_jip:atributy`).
verze 4.1:
  WS navíc oproti verzi 3.4 vrací osobní údaje uživatelů podle `§ 56a odst. 5 zákona č. 111/2009 Sb., o základních registrech <zr_>`_ (viz :ref:`api_jip:atributy`).
verze 4.2:
  WS navíc oproti verzi 4.1 vrací identifikátor SPUÚ z ROVM, pokud autentizovaný uživatel pochází ze SPUÚ a dále úroveň LoA pro NIA, pokud se uživatel autentizoval prostřednictvím NIA (viz :ref:`api_jip:atributy`).

.. _zr: https://www.e-sbirka.cz/sb/2009/111#par_56a-odst_5


Podrobnosti HTTP komunikace
---------------------------

Systémy CAAIS a AIS spolu komunikují pomocí protokolu HTTPS a předávají si zprávy Request-Response ve formátu SOAP 1.1. Při volání WS je nutné vkládat správné hodnoty do HTTP hlavičky ``SOAPAction`` dle přiložených WSDL souborů, jinak komunikace selže.


.. admonition:: Ukázka SOAP požadavku
   :class: note

   .. code:: http

    POST https://cert-externalauthapi.caais-test-ext.gov.cz/asws/atsEndpoint HTTP/1.1
    Host: cert-externalauthapi.caais-test-ext.gov.cz
    Accept: */*
    Accept-Encoding: gzip, deflate, br, zstd
    Content-Type: text/xml
    Content-Length: 172
    Connection: Keep-Alive
    SOAPAction: heartBeat
    User-Agent: python-requests/2.32.4

    <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
      <Header/>
      <Body>
        <heartBeatRequest xmlns="http://agw-as.cz/ats-ws/atsSzr/v4_2"/>
      </Body>
    </Envelope>

Povšimněte si hodnot HTTP hlaviček ``Content-Type`` a ``SOAPAction`` v ukázce.
    
Pro zabezpečení komunikace je dovoleno používat pouze šifrování protokolem TLS 1.2 či TLS 1.3, ostatní verze (SSL, TLS 1.0, TLS 1.1) nejsou povoleny. Pro volání WS je nutné AIS autentizovat klientským certifikátem při navázání mTLS spojení. Tento certifikát musí být zaregistrován v konfiguraci AIS v CAAIS a musí být vydán podporovanou certifikační autoritou (podrobnosti v části :ref:`si:certs`).

Jelikož JIP/KAAS legacy API využívá certifikát nejen k autentizaci, ale i k identifikaci konfigurace AIS v CAAIS, nelze použít stejný certifikát pro více konfigurací. Pokud by k tomu došlo, CAAIS se chová, jako by mu byl předkládán neznámý klientský certifikát. Jedna konfigurace však může mít registrováno více autentizačních certifikátů, čehož lze využít pro bezvýpadkovou výměnu certifikátů.

.. admonition:: Ukázka odpovědi při chybě certifikátu
   :class: note

   .. code:: http
   
      HTTP/1.1 401 
      Server: nginx
      Date: Sat, 23 Aug 2025 18:04:45 GMT
      Content-Type: application/json
      Transfer-Encoding: chunked
      Connection: keep-alive

      {"timestamp":"2025-08-23T18:04:45.910+00:00","status":401,"error":"Unauthorized","path":"/asws/atsEndpoint"}
      
Skutečně je chybová zpráva zapouzdřena do JSON, nikoli do XML.


Endpointy pro přístup ke službám
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Endpointy JIP/KAAS legacy API
   :header-rows: 1

   * - Účel
     - Prostředí
     - Adresa
      
   * - přihlášení
     - testovací
     - https://externalauthapi.caais-test-ext.gov.cz/login?atsId=exampleId
   * - přihlášení
     - produkční
     - https://externalauthapi.caais.gov.cz/login?atsId=exampleId
   * - odhlášení
     - testovací
     - https://externalauthapi.caais-test-ext.gov.cz/processLogout?atsId=exampleId&uri=adresa
   * - odhlášení
     - produkční
     - https://externalauthapi.caais.gov.cz/processLogout?atsId=exampleId&uri=adresa
   * - volání WS
     - testovací
     - https://cert-externalauthapi.caais-test-ext.gov.cz/asws/atsEndpoint
   * - volání WS
     - produkční
     - https://cert-externalauthapi.caais-test-ext.gov.cz/asws/atsEndpoint
     
Pokud jste připojeni do Centrálního místa služeb (CMS), použijete místo domény **gov.cz** doménu **cms2.cz**.

Hodnota parametru ``atsId`` obsahuje zkratku AIS z konfigurace CAAIS.

Po úspěšném přihlášení uživatele v CAAIS je uživatelův prohlížeč přesměrován na adresu registrovanou v konfiguraci AIS v CAAIS jako „URL po přihlášení“. Do URL je doplněn parametr ``sessionId``. Hodnotu tohoto parametru AIS využije při volání WS ``authConfirmation``.


.. _api_jip:odhlaseni:

V parametru ``uri`` se předává návratová adresa AIS, kam je uživatel přesměrován po odhlášení v CAAIS. Tato návratová URL adresa se v CAAIS porovnává s parametrem „URL pro odhlášení“ v konfiguraci AIS. Hodnoty v těchto parametrech se musí shodovat v začátku řetězce. Například je-li v konfiguraci AIS uložena hodnota *https\://www.example.org/logout/*, pak v parametru ``uri`` mohou být do CAAIS předány návratové adresy *https\://www.example.org/logout/?origin=caais* nebo *https\://www.example.org/logout/user/humphrey_appleby/*.


Metoda heartBeat
----------------

Metodu ``heartBeat`` je nutné volat jako SOAP operaci hearBeat, tedy s HTTP hlavičkou ``SOAPAction: heartBeat``.
Jmenný prostor v ukázkách níže odpovídá verzi 4.2 služeb. Pro jinou verzi služeb je nutné zvolit jiný jmenný prostor XML, viz  :ref:`api_jip:verze`.

Pro volání metody musí být navázáno mTLS spojení, při kterém se AIS jednoznačně identifikuje a autentizuje svým certifikátem registrovaným v CAAIS.
     
.. admonition:: Ukázka volání curl
   :class: note
   
   .. code:: sh
   
      #!/bin/zsh

      endpoint='https://cert-externalauthapi.caais-test-ext.gov.cz/asws/atsEndpoint'

      curl \
          --key key.pem --cert cert.pem -k \
          -H 'Content-Type: text/xml' \
          -H 'SOAPAction: heartBeat' \
          -d @heartbeat.soap-in.xml \
          $endpoint

.. admonition:: Ukázka dotazu (``heartbeat.soap-in.xml``)
   :class: note

   .. code:: xml
      
     <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
         <Header/>
         <Body>
             <heartBeatRequest xmlns="http://agw-as.cz/ats-ws/atsSzr/v4_2"/>
         </Body>
     </Envelope>


.. admonition:: Ukázka odpovědi
   :class: note

   .. code:: xml
   
      <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
          <SOAP-ENV:Header/>
          <SOAP-ENV:Body>
              <ns2:heartBeatResponse xmlns:ns2="http://agw-as.cz/ats-ws/atsSzr/v4_2">
                  <ns2:status>OK</ns2:status>
              </ns2:heartBeatResponse>
          </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>
      

Parametry a návratové hodnoty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Parametry ``heartBeatRequest``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam     
   * - —
     - —
     - *Volání nemá žádné parametry.*
     
     

.. list-table:: Návratové hodnoty ``heartBeatResponse``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam
   * - status
     - OK
     - Výsledek zpracování požadavku je OK.
   * - status
     - ERROR
     - Interní chyba systému CAAIS. Musí se buď počkat na vyřešení chyby nebo poslat požadavek znovu.

     
Metoda authConfirmation
-----------------------

Metodu ``authConfirmation`` je nutné volat jako nepojmenovanou SOAP operaci, tedy s HTTP hlavičkou ``SOAPAction: ‌``.
Jmenný prostor v ukázkách níže odpovídá verzi 4.2 služeb. Pro jinou verzi služeb je nutné zvolit jiný jmenný prostor XML, viz  :ref:`api_jip:verze`.

Pro volání metody musí být navázáno mTLS spojení, při kterém se AIS jednoznačně identifikuje a autentizuje svým certifikátem registrovaným v CAAIS.

.. admonition:: Ukázka volání curl
   :class: note
   
   .. code:: sh
   
      #!/bin/zsh
      
      endpoint='https://cert-externalauthapi.caais-test-ext.gov.cz/asws/atsEndpoint'
      session_id=$1
      
      curl \
          --key key.pem --cert cert.pem -k \
          -H 'Content-Type: text/xml' \
          -H 'SOAPAction: ' \
          -d '
              <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                <Body>
                  <authConfirmationRequest xmlns="http://agw-as.cz/ats-ws/atsSzr/v4_2">
                    <sessionId>'$session_id'</sessionId>
                  </authConfirmationRequest>
                </Body>
              </Envelope>' \
          -D - \
          $endpoint
          
.. admonition:: Ukázka dotazu
   :class: note
   
   .. code:: xml
   
      <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
          <authConfirmationRequest xmlns="http://agw-as.cz/ats-ws/atsSzr/v4_2">
            <sessionId>NBbUqwctW-Ri1fAUes9FsFhmueGsDmkaG5pSwENkZMWeqsQvIG</sessionId>
          </authConfirmationRequest>
        </Body>
      </Envelope>
   

.. admonition:: Ukázka odpovědi – neznámé sezení
   :class: note
   
   .. code:: xml
   
      <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
          <ns2:authConfirmationResponse xmlns:ns2="http://agw-as.cz/ats-ws/atsSzr/v4_2">
            <ns2:status>SESSION_NOT_FOUND</ns2:status>
          </ns2:authConfirmationResponse>
        </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>
      
      
.. admonition:: Ukázka odpovědi
   :class: note
   
   .. code:: xml
      
      <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
          <ns2:authConfirmationResponse xmlns:ns2="http://agw-as.cz/ats-ws/atsSzr/v4_2">
            <ns2:status>OK</ns2:status>
            <ns2:userRequestIp>0.0.0.0</ns2:userRequestIp>
            <ns2:attributes>
              <ns2:Username>humphrey_appleby</ns2:Username>
              <ns2:UzivatelId>MTZiMzM2NzAtYTgxNi00YzFhLTg3MTItZDk5ZTlmZjg1ZmVj</ns2:UzivatelId>
              <ns2:ZkratkaSubjektu>DIACZ</ns2:ZkratkaSubjektu>
              <ns2:IcSubjektu>17651921</ns2:IcSubjektu>
              <ns2:Jmeno>Humphrey</ns2:Jmeno>
              <ns2:Prijmeni>Appleby</ns2:Prijmeni>
              <ns2:TitulPred>Sir</ns2:TitulPred>
              <ns2:TitulZa/>
              <ns2:PristupoveRole>
                <ns2:role>USER</ns2:role>
                <ns2:role>ADMIN</ns2:role>
              </ns2:PristupoveRole>
              <ns2:CinnostniRole/>
              <ns2:Email>humphrey.appleby@dia.gov.cz</ns2:Email>
              <ns2:NazevSubjektu>Digitální a informační agentura</ns2:NazevSubjektu>
              <ns2:EmailSubjektu/>
              <ns2:TypInstituce>11</ns2:TypInstituce>
              <ns2:OvmPrimarni/>
              <ns2:TypPrihlaseni>p-pwd</ns2:TypPrihlaseni>
              <ns2:TypPrihlaseniNia>http://eidas.europa.eu/LoA/low</ns2:TypPrihlaseniNia>
              <ns2:OsobaZtotoznena>false</ns2:OsobaZtotoznena>
              <ns2:Pracoviste/>
              <ns2:MistoNarozeni/>
              <ns2:Doklady/>
              <ns2:NeevidovatOsobniUdaje>false</ns2:NeevidovatOsobniUdaje>
              <ns2:IdentifikatorOvm>17651921</ns2:IdentifikatorOvm>
              <ns2:IdentifikatorSpuu/>
              <ns2:TimeLimitedId>0814a3b3-509a-4dc2-bcd3-7cf016141404</ns2:TimeLimitedId>
            </ns2:attributes>
          </ns2:authConfirmationResponse>
        </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>


.. list-table:: Parametry ``authConfirmationRequest``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam     
   * - sessionId
     - *náhodný řetezec*
     - Identifikace uživatelské session. Jedná se o autentizační token vygenerovaný v CAAIS a předaný do AIS při přesměrování uživatele.
     
     

.. list-table:: Návratové hodnoty ``authConfirmationResponse``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam
   * - status
     - OK
     - Výsledek zpracování požadavku je OK.
   * - status
     - SESSION_NOT_FOUND
     - Chyba v případě, že byl v požadavku předán neexistující token.
   * - status
     - SYSTEM_ERROR
     - Interní chyba systému CAAIS. Musí se buď počkat na vyřešení chyby nebo poslat požadavek znovu.
   * - userRequestIp
     - 0.0.0.0
     - IP adresa uživatele při přihlášení. Může být IPv6/IPv4. Pokud uživatel využívá proxy pro přístup, předává se IP proxy, která je nejdále od uživatele. V CAAIS vždy 0.0.0.0.
   * - attributes
     - :ref:`api_jip:tabulka-atributy`
     - Údaje o autentizovaném uživateli.


.. _api_jip:atributy:
     
Seznam atributů uživatele
~~~~~~~~~~~~~~~~~~~~~~~~~

JIP/KAAS legacy API je (s výhradou změny jmenného prostoru) zpětně kompatibilní se svými staršími verzemi: Atributy představené v dřívějších verzích jsou dostupné i ve verzích pozdějších. Sloupec verze v tabulce níže tak označuje první verzi JIP/KAAS legacy API, kde lze daný atribut získat.

.. _api_jip:tabulka-atributy:
.. list-table:: Seznam atributů uživatele v odpovědi
   :header-rows: 1
   
   * - Verze
     - Atribut
     - Popis
     - Atribut z datového modelu
   * - 2.1
     - ZkratkaSubjektu
     - Zkratka subjektu, pod který patří uživatel. Jde o jedinečné ID subjektu v systému CAAIS.
     - "Subjekt"."zkratka" (Subject.shortcut)
   * - 2.1
     - IcSubjektu
     - IČ subjektu, pod který patří uživatel.
     - "Subjekt"."ič" (Subject.identificationNumber)
   * - 2.1
     - UzivatelId
     - Jedinečné ID uživatele (profilu) v systému CAAIS.
     - "Mapování SeP"." SePBSI" (ServiceMapping.sepBsi) pro daný "Profil"."uživatelské jméno" (Profile.loginName);  BSI se generuje v CAAIS vždy nové, nemigruje se z JIP/KAAS.
   * - 2.1
     - Username
     - Uživatelské jméno uživatele (profilu) v systému CAAIS.
     - "Profil"."uživatelské jméno" (Profile.loginName)
   * - 2.1
     - Jmeno
     - Jméno 
     - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
   * - 2.1
     - Prijmení
     - Příjmení 
     - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
   * - 2.1
     - TitulPred
     - Titul před jménem
     - "Profil"."Fyzická osoba"."titul před" (Profile.PhysicalPerson.degreeBefore)
   * - 2.1
     - TitulZa
     - Titul za jménem
     - "Profil"."Fyzická osoba"."titul za" (Profile.PhysicalPerson.degreeAfter)
   * - 2.1
     - PristupoveRole
     - Seznam přístupových rolí do AIS přiřazených uživateli.
     - "Profil"."Přístupová role" (Profile.AccessRole)
        Pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu. Pokud má profil přiřazeny Skupiny rolí nebo Organizační role, dotahují se přes ně odpovídající přístupové role. Dále se dotahují i delegované přístupové role přes "Vazební profil".
        V seznamu přístupových rolí se vrací pouze role pro daný AIS, do kterého se uživatel autentizuje.
   * - 2.1
     - …/role
     - Kód přístupové role.
     - "Přístupová role"."zkratka" (AccessRole.shortcut)
   * - 2.1
     - CinnostniRole
     - Seznam činnostních rolí přiřazených uživateli.
     - "Profil"."Činnostní role" (Profile.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu

        Pokud má profil přiřazeny Skupiny rolí nebo Business role dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".
   * - 2.1
     - …/KodAgendy
     - Kód agendy činnostní role.
     - "Činnostní role"."Agenda"."kód" (ActivityRole.Agenda.code)
   * - 2.1
     - …/KodCinnostniRole
     - Kód činnostní role.
     - "Činnostní role"."kód" (ActivityRole.code)
   * - 3.4
     - Email
     - Email uživatele.
     - "Profil"."email" (Profile.email)
     
   * - 3.4
     - NazevSubjektu
     - Název subjektu, pod který patří uživatel.
     - "Subjekt"."název" (Subject.name)
   * - 3.4
     - EmailSubjektu
     - Email subjektu.
     - "Subjekt"."Kontakt"."Email"."adresa" (Subject.Contact.Email.address) kde "Email"."Typ emailu"."název" (Email.EmailType.name) = "Oficiální"
   * - 3.4
     - TypInstituce
     - Typ instituce pro subjekt. Číselník viz kap. 6.1.
     - "Subjekt"."Typ instituce"."kód" (Subject.InstitutionType.code)
   * - 3.4
     - OvmPrimarni
     - Hlavní subjekt pro subjekty s duplicitním IČ (hodnoty true/false).
     - *neexistuje*
   * - 3.4
     - TypPrihlaseni
     - Způsob přihlášení uživatele. Viz :ref:`api_jip:ciselnik:prihlaseni`.
     - Viz :ref:`api_jip:ciselnik:prihlaseni`.
   * - 4.2
     - TypPrihlaseniNia
     - Hodnota LoA použitého identifikačního prostředku, pokud uživatel použil autentizaci přes NIA.
     - Hodnota z výčtu: 
     
       - http\://eidas.europa.eu/LoA/low
       - http\://eidas.europa.eu/LoA/substantial
       - http\://eidas.europa.eu/LoA/high
   * - 3.4
     - OsobaZtotoznena
     - Příznak, že byla fyzická osoba (uživatel) ztotožněn v ROB.
     - "Profil"."Fyzická osoba"."osoba evidována v rob" (Profile.PhysicalPerson.personInRob)
   * - 3.4
     - TokenAifo
     - Datová struktura pro získání AIFO fyzické osoby (kódování Base64). Aktuálně se nic nevrací (v ROB není implementována odpovídající WS).
     - *neexistuje*
   * - 3.4
     - Pracoviste
     - Pracoviště uživatele.
     - *neexistuje*
   * - 3.4
     - …/Id
     - Identifikátor pracoviště
     - *neexistuje*
   * - 3.4
     - …/Nazev
     - Název pracoviště
     - *neexistuje*
   * - 3.4
     - …/Adresa
     - Adresa pracoviště
     - *neexistuje*
   * - 3.4
     - …/KodAdresy
     - Kód adresy RUIAN pro pracoviště.
     - *neexistuje*
   * - 4.1
     - Mistonarozeni
     - Místo narození uživatele.
     - Pokud "Profil"."Fyzická osoba"."Místo narození"."Stát"."kód" (Profile.PhysicalPerson.BirthPlace. Country.code) = 203 (tzn. jedná se o ČR) vyplňuje se atribut WS MistoNarozeniCr, jinak se vyplňuje atribut WS MistoNarozeniSvet
   * - 4.1     
     - …/MistoNarozeniCr
     - Pokud je uživatel narozen v ČR, je uveden kód místa z RUIAN.
       Další atributy v elementu:
       
       - "mop" – příznak, zda se jedná o kód městského obvodu
       - "nazev" – název místa narození v ČR
     - "Místo narození"."Obec"."kód" (BirthPlace.Municipality.code)
       
       Pokud "Místo narození"."Obec"."pražský obvod" (BirthPlace.Municipality.praguePart) = 1 , vyplní se atribut WS "mop" = true.

       "Místo narození"."Obec"."název" (BirthPlace.Municipality.name) se vyplní do atributu WS "nazev".
   * - 4.1     
     - …/MistoNarozeniSvet
     - Název místa narození v zahraničí.
     -
   * - 4.1
     - …/…/stat
     - Kód státu. Číselník států ze Správy základních registrů.
       Další atributy v elementu: "nazev" – název státu.
     - "Místo narození"."Stát"."kód" (BirthPlace.Country.code)
     
       "Místo narození"."Stát"."krátký název" (BirthPlace.Country.shortName) se vyplní do atributu WS "nazev".
   * - 4.1
     - …/…/misto
     - Název místa narození v zahraničí.
     - "Místo narození"."název" (BirthPlace.name)
   * - 4.1     
     - DatumNarozeni
     - Datum narození.
     - "Profil"."Fyzická osoba"."datum narození" (Profile.PhysicalPerson.birthDate)
   * - 4.1
     - DatumUmrti
     - Datum úmrtí.
     - "Profil"."Fyzická osoba"."datum úmrtí" (Profile.PhysicalPerson.deathDate)
   * - 4.1
     - Doklady
     - Seznam dokladů.
     - V CAAIS je pouze 1 doklad.
   * - 4.1
     - …/Doklad
     - Číslo dokladu.
       Další atributy v elementu: "typ" – druh dokladu, dle číselníku typů dokladů ze Správy základních registrů.
     - "Profil"."Fyzická osoba"."druh dokladu" (Profile.PhysicalPerson.documentType) a
     
       "Profil"."Fyzická osoba"."číslo dokladu" (Profile.PhysicalPerson.documentId)
   * - 4.1
     - NeevidovatOsobniUdaje
     - Příznak, že je zakázáno pro daného uživatele evidovat osobní údaje.
     - *neexistuje*
   * - 3.4
     - IdentifikatorOvm
     - Identifikátor OVM z ROVM.
     - "Subjekt"."kód ovm v rovm" (Subject.ovmInRovmCode)
   * - 4.2
     - IdentifikatorSpuu
     - Identifikátor SPUÚ z ROVM.
     - "Subjekt"."kód spuú" (Subject.spuuCode)
   * - 3.4
     - TimeLimitedId
     - Speciální autorizační token s omezenou dobou platnosti pro přístup k vybraným WS. Vrací se pouze pokud je uživatel lokální administrátor.
     - Technický atribut pro ukládání tokenů (neuveden v datovém modelu)
