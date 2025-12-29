.. _api_jip:techspec_prima:

Technická specifikace přímé autentizace
==========================================

.. include:: deprecation-warning.inc.rst

Jde o WS, která zajišťuje ověření uživatele pomocí jednorázových přihlašovacích údajů. Tyto údaje uživateli vygeneroval systém CAAIS na základě provedeného přihlášení uživatele do CAAIS (pomocí skutečných přihlašovacích údajů do CAAIS-IdP, nebo prostřednictvím NIA).

Účelem této přímé autentizační WS tedy není ověřovat skutečné přihlašovací údaje, které jsou uloženy v CAAIS-IdP, ale ověřit ty jednorázové. V případě, že jsou zadány skutečné přihlašovací údaje, přímá autentizační WS vyhodnotí pokus jako neúspěšný.

.. admonition:: Přímá a klasická metoda autentizace
   :class: note
   
   Kromě rozdílu v úvodním ověření uživatele jsou si přímá a klasická metoda JIP/KAAS legacy autentizace velice podobné. Tato kapitola proto popisuje jen důležité odchylky. Hlavní text se nachází v kapitole věnované :ref:`klasické JIP/KAAS legacy autentizaci <api_jip:techspec>`.
   


Verze JIP/KAAS legacy API
-------------------------

JIP/KAAS legacy API využívá SOAP protokol verze 1.1. CAAIS k udržení maximální kompatibility s JIP/KAAS podporuje několik verzí jeho API.

.. _api_jip:verze_prima:
.. list-table:: Verze JIP/KAAS legacy API
   :header-rows: 1

   * - Veze
     - WSDL
     - XMLNS
   * - 3.4
     - :download:`DirectAuth_v3_4 <_static/wsdl/DirectAuth_v3_4.wsdl>`
     - http\://agw-as.cz/ats-ws/atsUser/atsSzr/v3_4
   * - 4.1
     - :download:`DirectAuth_v4_1 <_static/wsdl/DirectAuth_v4_1.wsdl>`
     - http\://agw-as.cz/ats-ws/atsUser/atsSzr/v4_1
   * - 4.2
     - :download:`DirectAuth_v4_2 <_static/wsdl/DirectAuth_v4_2.wsdl>`
     - http\://agw-as.cz/ats-ws/atsUser/atsSzr/v4_2
     
Ve WSDL souborech jsou vždy uvedeny URL endpointu pro produkční prostředí CAAIS. Pokud je potřeba použít jiné prostředí, je nutné ručně URL upravit.

API ve všech verzích implementuje právě jednu metodu ``directAuthUser``, jak je popsáno ve WSDL souborech. API se liší jmenným prostorem XML, jinak není ve volání metod mezi jednotlivými verzemi rozdíl, pouze se zvětšuje množina údajů vracená v odpovědi ``directAuthUser``, více :ref:`api_jip:atributy`.

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


Pro zabezpečení komunikace je dovoleno používat pouze šifrování protokolem TLS 1.2 či TLS 1.3, ostatní verze (SSL, TLS 1.0, TLS 1.1) nejsou povoleny. Pro volání WS je nutné AIS autentizovat klientským certifikátem při navázání mTLS spojení. Tento certifikát musí být zaregistrován v konfiguraci AIS v CAAIS a musí být vydán podporovanou certifikační autoritou (podrobnosti v části :ref:`si:certs`).

Endpointy pro přístup ke službám
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Endpointy JIP/KAAS legacy API
   :header-rows: 1

   * - Účel
     - Prostředí
     - Adresa
      
   * - přihlášení
     - testovací
     - https://externalauthapi.caais-test-ext.gov.cz/login?atsId=exampleId&providerType=directAuth
   * - přihlášení
     - produkční
     - https://externalauthapi.caais.gov.cz/login?atsId=exampleId&providerType=directAuth
   * - odhlášení
     - testovací
     - https://externalauthapi.caais-test-ext.gov.cz/processLogout?atsId=exampleId&uri=adresa
   * - odhlášení
     - produkční
     - https://externalauthapi.caais.gov.cz/processLogout?atsId=exampleId&uri=adresa
   * - volání WS
     - testovací
     - https://cert-externalauthapi.caais-test-ext.gov.cz/asws/directAuthUserEndpoint
   * - volání WS
     - produkční
     - https://cert-externalauthapi.caais.gov.cz/asws/directAuthUserEndpoint

     
Pokud jste připojeni do Centrálního místa služeb (CMS), použijete místo domény **gov.cz** doménu **cms2.cz**.

Hodnota parametru ``atsId`` obsahuje zkratku AIS z konfigurace CAAIS. Pro odlišení od klasické autentizace je dále nutné uvádět parametr ``providerType=directAuth``. Uživateli je po přihlášení zobrazeno jednorázové uživatelské jméno a heslo s platností 30 minut.

Endpoint pro odhlášení :ref:`se shoduje s klasickou JIP/KAAS legacy autentizací <api_jip:odhlaseni>`.

     
Metoda directAuthUser
-----------------------


.. admonition:: Ukázka volání curl
   :class: note
   
   .. code:: sh
   
      #!/bin/zsh
      
      endpoint='https://cert-externalauthapi.caais-test-ext.gov.cz/asws/directAuthUserEndpoint'
      username=$1
      password=$2
      
      curl \
          --key key.pem --cert cert.pem -k \
          -H 'Content-Type: text/xml' \
          -H 'SOAPAction: directAuthUserv2' \
          -d '
              <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                <Body>
                  <directAuthUserRequest xmlns="http://agw-as.cz/ats-ws/atsUser/atsSzr/v4_2">
                    <username>'$username'</username>
                    <password>'$password'</password>
                  </directAuthUserRequest>
                </Body>
              </Envelope>' \
          -D - \
          $endpoint

.. admonition:: Ukázka dotazu
   :class: note
  
   .. code:: xml
   
      <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
          <directAuthUserRequest xmlns="http://agw-as.cz/ats-ws/atsUser/atsSzr/v4_2">
            <username>caais_user_2362685776</username>
            <password>81R:t=cD+RHBAQrO-Qax</password>
          </directAuthUserRequest>
        </Body>
      </Envelope>

.. admonition:: Ukázka odpovědi
   :class: note
  
   .. code:: xml

    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
      <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
          <ns2:directAuthUserResponse xmlns:ns2="http://agw-as.cz/ats-ws/atsUser/atsSzr/v4_2">
            <ns2:attributes>
              <ns2:Username>humphrey_appleby</ns2:Username>
              <ns2:UzivatelId>MTZiMzM2NzAtYTgxNi00YzFhLTg3MTItZDk5ZTlmZjg1ZmVj</ns2:UzivatelId>
              <ns2:ZkratkaSubjektu>DIACZ</ns2:ZkratkaSubjektu>
              <ns2:IcSubjektu>17651921</ns2:IcSubjektu>
              <ns2:Jmeno>Humphrey</ns2:Jmeno>
              <ns2:Prijmeni>Appleby</ns2:Prijmeni>
              <ns2:TitulPred>Sir</ns2:TitulPred>
              <ns2:TitulZa/>
              <ns2:PristupoveRole/>
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
              <ns2:Doklady/>
              <ns2:NeevidovatOsobniUdaje>false</ns2:NeevidovatOsobniUdaje>
              <ns2:IdentifikatorOvm>17651921</ns2:IdentifikatorOvm>
              <ns2:IdentifikatorSpuu/>
              <ns2:TimeLimitedId>723e81cb-02f8-4872-8b9d-30326f895d7a</ns2:TimeLimitedId>
            </ns2:attributes>
          <ns2:status>OK</ns2:status>
        </ns2:directAuthUserResponse>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>

    
.. list-table:: Parametry ``authDirectUserRequest``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam     
   * - username
     - caais_user_xxxxxxxxxx
     - Jednorázové uživatelské jméno.
   * - password
     - 
     - Jednorázové uživatelské heslo.
     
Jednorázové uživatelské jméno a heslo mají omezenou platnost na 30 minut.

.. list-table:: Parametry ``authDirectUserResponse``
   :widths: 10 10 100
   :header-rows: 1
   
   * - Element
     - Hodnota
     - Význam     
   * - status
     - OK
     - Ověření uživatele proběhlo OK. Uživatel se zadanými přihlašovacími údaji v CAAIS existuje.
   * - status
     - VERIFICATION_FAILED
     - Ověření uživatele bylo neúspěšné (nesprávné přihlašovací údaje).
   * - status
     - SYSTEM_ERROR
     - Interní chyba systému CAAIS. Musí se buď počkat na vyřešení chyby nebo poslat požadavek znovu.
   * - description
     -
     - Detailní popis výsledku zpracování žádosti. Při chybě je vložena chybová hláška.
   * - userRequestIp
     - 
     - IP adresa uživatele při přihlášení. Může být IPv6/IPv4. Pokud uživatel využívá proxy pro přístup, předává se IP proxy, která je nejdále od uživatele.
   * - attributes
     - :ref:`api_jip:tabulka-atributy`
     - Údaje o autentizovaném uživateli.

Definice :ref:`atributů <api_jip:tabulka-atributy>` se neliší od těch obsažených v elementu ``authConfirmationResponse`` klasické JIP/KAAS legacy autentizace. 
