.. _ws:edit-1:

=================================================================
Metody webové služby pro čtení a zápis údajů subjektu (WS-EDIT/1)
=================================================================

Metody pro správu dat jsou dostupné jak ve webové službě **verze 1.1**, tak **verze 1.0**. Podrobně je syntaxe metod popsána ve schématech:

- :download:`XSD editačních služeb 1.0<_static/xsd/ws-10.xsd>`,
- :download:`XSD editačních služeb 1.1, část 1<_static/xsd/ws-11-1.xsd>`.

Metody ve verzi 1.1 se od metod ve verzi 1.0 liší jmenným prostorem (viz :ref:`ws:edit-1:ns`) a přidáním několika nových atributů. Příklady v tomto dokumentu zachycují metody ve verzi 1.1 editačních webové služby; pro verzi 1.0 je potřeba zaměnit xmlns.

.. contents:: Metody WS-EDIT/1
   :local:
   :depth: 2

.. _ws:edit-1:ns:

.. list-table:: Jmenné prostory metod WS-EDIT/1
   :header-rows: 1

   * - Verze
     - XMLNS
     - Endpoint [#endpoint]_
   * - 1.0
     - http\://userportal.novell.com/ws/WS-LA-1.0
     - https://externaleditapi10.caais.gov.cz/spravadat/ws/call/exampleId
   * - 1.1
     - http\://userportal.novell.com/ws/WS-LA-1.1
     - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/1/call/exampleId
     
.. [#endpoint] zde jsou uvedeny jen příklady endpointů; v úplnosti :ref:`ws10:endpoints` a :ref:`ws11:endpoints`
     
Pokud XSD definuje určité atributy odpovědi jako volitelné, ale CAAIS je nikdy nevrací nebo je vrací vždy prázdné – například protože nejsou obsaženy v jeho datovém modelu – nejsou pro přehlednost v příkladech a seznamech atributů níže uváděny. Atributy označené jako :bdg-primary:`WS 1.1` jsou dostupné jen při využití verze 1.1 webové služby.

.. _ws:common:

Společné typy a hodnoty
=======================

**Přístupové role** jsou uváděny vždy v tečkové notaci *<zkratka_ais>.<zkratka_pristupove_role>*, například *example_ais.example_role_1*.

**Časová razítka poslední změny** (aribut ``casPosledniZmeny``) jsou uváděny celočíselně ve formátu Unix timestamp, tedy jako celý počet sekund od půlnoci 1. ledna 1970 UTC bez ohledu na přestupné sekundy.

**Poštovní adresa** je složený element, jak je uvedeno v tabulce :ref:`ws:adresa`.

.. _ws:adresa:

.. list-table:: Popis atributů v adrese
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - …/addressCode
     - Kód adresního místa z RUIAN
     - "Adresa"."kód adresy" (Address.addressCode)
   * - …/street
     - Název ulice
     - "Adresa"."název ulice" (Address.streetName)
   * - …/cityCode
     - Kód obce
     - "Adresa"."Obec"."kód" (Address.Municipality.code)
   * - …/city
     - Název obce
     - "Adresa"."Obec"."název" (Address.Municipality.name)
   * - …/region
     - Název kraje
     - "Adresa"."Kraj"."název" (Address.Region.name)
   * - …/postalCode
     - PSČ
     - "Adresa"."psč" (Address.zipCode)
   * - …/metropolitanDistrict
     - Název městské části nebo městského obvodu (údaj MOMC v RUIAN)
     - "Adresa"."název městské části" (Address.cityPartName)
   * - …/cityPart
     - Název části obce nebo katastrálního území hl. m. Prahy
     - "Adresa"."název části obce" (Address.municipalityPartName)
   * - …/houseNumber
     - Číslo popisné
     - "Adresa"."číslo popisné" (Address.houseNumber) nebo "Adresa"."číslo evidenční" (Address.evidenceNumber) podle toho, které z čísel je vyplněno
   * - …/sequenceNumber
     - Číslo orientační
     - "Adresa"."číslo orientační" (Address.sequenceNumber)
   * - …/buildingType
     - V případě budovy s číslem evidenčním je nastaven na hodnotu 2.
     - = 2, pokud je vyplněn parametr "Adresa"."číslo evidenční" (Address.evidenceNumber), jinak prázdné 
   * - ../pragueDistrict
     - Název městského obvodu hl. m. Prahy (údaj MOP v RUIAN)
     - "Adresa"."název městského obvodu Praha" (Address.praguePartName)
     
.. _ws:common:update:

Aktualizace údajů
-----------------

Při aktualizaci údajů (update request) se množinové elementy (seznamy) nastavují vždy jako celá množina, nikoli změnově. Je-li *N* nastavovaná množina a *P* původní množina, pak prvky v rozdílu *N* ∖ *P* jsou přidány a prvky v rozdílu *P* ∖ *N* odebrány. 


Verze webové služby
===================


.. _ws:getversion:

GetVersion
----------

Metoda GetVersion na základě požadavku ``GetVersionRequest`` vrací v odpovědí ``GetVersionResponse`` verzi webové služby.

.. admonition:: Příklad žádosti GetVersionRequest (verze 1.0)
   :class: info

   .. code:: xml

      <GetVersionRequest xmlns="http://userportal.novell.com/ws/WS-LA-1.0"/>

.. admonition:: Příklad odpovědi GetVersionResponse (verze 1.0)
   :class: info

   .. code:: xml

      <ns2:GetVersionResponse xmlns:ns2="http://userportal.novell.com/ws/WS-LA-1.0">WS-LA-1.0</ns2:GetVersionResponse>

.. admonition:: Příklad žádosti GetVersionRequest (verze 1.1)
   :class: info

   .. code:: xml

      <GetVersionRequest xmlns="http://userportal.novell.com/ws/WS-LA-1.1"/>

.. admonition:: Příklad odpovědi GetVersionResponse (verze 1.1)
   :class: info

   .. code:: xml

      <ns2:GetVersionResponse xmlns:ns2="http://userportal.novell.com/ws/WS-LA-1.1">WS-LA-1.1</ns2:GetVersionResponse>


Správa subjektů
===============

.. _ws:getsubject:

GetSubject
----------

Metoda GetSubject na základě požadavku ``GetSubjectRequest`` vrací v odpovědi ``GetSubjectResponse`` údaje daného subjektu (plyne z URL endpointu).

.. admonition:: Příklad žádosti GetSubjectRequest
   :class: info
   
   .. literalinclude:: _static/xml/GetSubjectRequest.xml
      :language: xml


.. admonition:: Příklad odpovědi GetSubjectResponse
   :class: info
   
   .. literalinclude:: _static/xml/GetSubjectResponse.xml
      :language: xml

.. list-table:: Popis atributů ``GetSubjectResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - isdsBox
     - ID hlavní datové schránky
     - "Datová schránka"."id datové schránky" (DataBox.dataBoxId)
   * - name
     - Oficiální název subjektu
     - "Subjekt"."název" (Subject.name)
   * - ico
     - IČ subjektu
     - "Subjekt"."ič" (Subject.identificationNumber)
   * - dic
     - DIČ
     - "Subjekt"."dič" (Subject.vatId)
   * - datumVzniku
     - Datum vzniku subjektu
     - "Subjekt"."datum vzniku" (Subject.creationDate)
   * - datumZaniku
     - Datum zániku subjektu
     - "Subjekt"."datum zániku" (Subject.expirationDate)
   * - preruseniPozastaveniOd
     - Datum přerušení/pozastavení od
     - "Subjekt"."datum přerušení/pozastavení od" (Subject.suspensionDateFrom)
   * - preruseniPozastaveniDo
     - Datum přerušení/pozastavení do
     - "Subjekt"."datum přerušení/pozastavení do" (Subject.suspensionDateTo)
   * - preruseniPozastaveni
     - Přerušení/pozastavení
     - "Subjekt"."přerušení/pozastavení" (Subject.suspended)
   * - zruseno
     - Značí, že subjekt byl zrušen.
     - TRUE – pokud "Subjekt"."datum zániku" (Subject.expirationDate) <= sysdate, FALSE – jinak
   * - casZruseni
     - Čas zrušení subjektu.
     - "Subjekt"."datum zániku" (Subject.expirationDate)
   * - isOVM
     - Značí, že subjekt je OVM/SPUU, je čerpáno z ROVM
     - TRUE – pokud "Subjekt"."Typ subjektu" (Subject.SubjectType) = OVM, FALSE – jinak
   * - rovmCode
     - Kód OVM v ROVM
     - "Subjekt"."kód ovm v rovm" (Subject.ovmInRovmCode)
   * - spuuCode
     - Kód SPUU
     - "Subjekt"."kód spuú" (Subject.spuuCode)
   * - rovmPusobnostOd
     - Působnost v ROVM od
     - "Subjekt"."Rovm"."působnost od" (Subject.Rovm.activityFrom)
   * - rovmPusobnostDo
     - Působnost v ROVM do
     - "Subjekt"."Rovm"."působnost do" (Subject.Rovm.activityTo)
   * - rovmPozastaveniOd
     - Pozastavení v ROVM od
     - "Subjekt"."Rovm"."pozastavení od" (Subject.Rovm.suspensionFrom)
   * - rovmPozastaveniDo
     - Pozastavení v ROVM do
     - "Subjekt"."Rovm"."pozastavení do" (Rovm.suspensionTo)
   * - rovmPreruseniOd
     - Přerušení v ROVM od
     - "Subjekt"."Rovm"."přerušení od" (Subject.Rovm.interruptionFrom)
   * - rovmPreruseniDo
     - Přerušení v ROVM do
     - "Subjekt"."Rovm"."přerušení do" (Subject.Rovm.interruptionTo)
   * - rovmKategorie
     - Kategorie v ROVM
     - "Subjekt"."Rovm"."Kategorie v ROVM" (Subject.Rovm.RovmCategory)
   * - …/code
     - Kód kategorie v ROVM
     - "Kategorie v ROVM"."kód" (RovmCategory.code)
   * - pravniForma
     - Kód právní formy subjektu podle číselníku ROS.
     - "Subjekt"."Právní forma"."kód" (Subject.LegalForm.code)
   * - …/text
     - Název právní formy (volitelně)
     - "Subjekt"."Právní forma"."název" (Subject.LegalForm.name)
   * - typInstituce
     - Typ instituce
     - "Subjekt"."Typ instituce"."kód" (Subject.InstitutionType.code)
   * - …/text
     - Název typu instituce (volitelně)
     - "Subjekt"."Typ instituce"."název" (Subject.InstitutionType.name)
   * - gpsPosition
     - GPS souřadnice vázané na adresu úřadu
     - "Subjekt"."Kontakt"."Adresa"."gps souřadnice x" + "gps souřadnice y" (Subject.Contact.Address.gpsx + gpsy) – vazba "adresa úřadu" (officeAddress)
   * - contactAddress
     - Adresa
     - "Subjekt"."Kontakt"."Adresa" (Subject.Contact.Address) – vazba "adresa úřadu" (officeAddress); :ref:`ws:common`. 
   * - contactAddressPostalCode
     - Poštovní směrovací číslo přidělené pro účely úřadu
     - "Subjekt"."Kontakt"."psč úřadu" (Subject.Contact.officeZipCode)
   * - contactAddressPoBoxCode
     - Číslo poštovní přihrádky
     - "Subjekt"."Kontakt"."p.o. box úřadu" (Subject.Contact.officePoBox)
   * - deliveryAddress
     - Kontaktní poštovní adresa
     - "Subjekt"."Kontakt"."Adresa" (Subject.Contact.Address) - vazba "kontaktní poštovní adresa" (contactPostalAddress); :ref:`ws:common`
   * - deliveryAddressPostalCode
     - Poštovní směrovací číslo kontaktní poštovní adresy přidělené pro účely úřadu
     - "Subjekt"."Kontakt"."psč úřadu poštovní adresy" (Subject.Contact.postalAddressZipCode)
   * - deliveryAddressPoBoxCode
     - Číslo poštovní přihrádky kontaktní poštovní adresy
     - "Subjekt"."Kontakt"."p.o. box úřadu poštovní adresy" (Subject.Contact.postalAdressPoBox)
   * - email
     - Seznam kontaktních e-mailů
     - "Subjekt"."Kontakt"."Email" (Subject.Contact.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/text
     - Název typu emailu
     - "Email"."Typ emailu"."název" (Email.EmailType.name)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel
     - "Subjekt"."Kontakt"."Telefon" (Subject.Contact.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/text
     - Název typu telefonu
     - "Telefon"."Typ Telefonu"."název" (PhoneNumber.PhoneNumberType.name)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - bankAccount
     - Bankovní spojení. Obsahuje 4-číselný kód banky a číslo účtu.
     - "Subjekt"."Bankovní spojení" (Subject.BankAccount)
   * - …/number
     - Číslo účtu
     - "Bankovní spojení"."číslo účtu" (BankAccount.number)
   * - …/bankCode
     - Kód banky
     - "Bankovní spojení"."kód banky" (BankAccount.bankCode)
   * - …/description
     - Popis
     - "Bankovní spojení"."popis" (BankAccount.description)
   * - Url
     - WWW odkaz.
     - "Subjekt"."Url WWW" (Subject.WwwUrl)
   * - …/url
     - URL adresa
     - "Url WWW"."url" (WwwUrl.url)
   * - …/description
     - Poznámka
     - "Url WWW"."poznámka" (WwwUrl.note)
   * - …/type
     - Kód typu URL
     - "Url WWW"."Typ URL"."kód" (WwwUrl.UrlType.code)
   * - …/text
     - Název typu URL
     - "Url WWW"."Typ URL"."název" (WwwUrl.UrlType.name)
   * - isdsBoxState
     - Stav hlavní datové schránky subjektu.
     - "Subjekt"."Datová schránka"."stav datové schránky" (Subject.DataBox.dataBoxState)
   * - isdsBoxChangeTime
     - Čas poslední změny datové schránky.
     - "Subjekt"."Datová schránka"."čas poslední změny" (Subject.DataBox.lastChangeTime)
   * - prijataPusobnostVolby
     - Seznam veřejnoprávních smluv s obcemi, které přenesly svoji působnost na subjekt.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „cílovým subjektem“ a kde „Typ působnosti“ = „Pro volby“
   * - …/subject
     - Zkratka obce (jiného subjektu), který přenesl svoji působnost na subjekt.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "zdrojový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - predanaPusobnostVolby
     - Seznam veřejnoprávních smluv s obcemi, na které subjekt přenesl svoji působnost.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „zdrojovým subjektem“ a kde „Typ působnosti“ = „Pro volby“
   * - …/subject
     - Zkratka obce (jiného subjektu), na který subjekt přenesl svoji působnost.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "cílový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - …/reason
     - Důvod předané působnosti.
     - "Působnost"."důvod" (Authority.reason)
   * - prijataPusobnostAdmin
     - Seznam veřejnoprávních smluv s obcemi, které přenesly svoji působnost na subjekt.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „cílovým subjektem“ a kde „Typ působnosti“ = „Lokální administrátor“
   * - …/subject
     - Zkratka obce (jiného subjektu), který přenesl svoji působnost na subjekt.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "zdrojový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - predanaPusobnostAdmin
     - Seznam veřejnoprávních smluv s obcemi, na které subjekt přenesl svoji působnost.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „zdrojovým subjektem“ a kde „Typ působnosti“ = „Lokální administrátor“
   * - …/subject
     - Zkratka obce (jiného subjektu), na který subjekt přenesl svoji působnost.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "cílový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - …/reason
     - Důvod předané působnosti.
     - "Působnost"."důvod" (Authority.reason)
   * - aisRole
     - Seznam rolí pro přístup do aplikací přidělených subjektu
     - "Subjekt"."Přístupová role" (Subject.AccessRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu
   * - …/item
     - Zkratka role
     - "Přístupová role"."zkratka" (AccessRole.shortcut); hodnota atributu je :ref:`ve formátu <ws:common>`: <zkratka_ais>.<zkratka_pristupove_role>.
   * - …/text
     - Název role
     - "Přístupová role"."název" (AccessRole.name)
   * - agendy
     - Seznam agend z RPP, které se vztahují k agendovým činnostním rolím.
     - "Subjekt"."Činnostní role"."Agenda" (Subject.ActivityRole.Agenda) – pouze ty agendy, jejichž činnostní role jsou aktivní a mají aktivní přiřazení subjektu
   * - …/item
     - Kód agendy
     - "Agenda"."kód" (Agenda.code)
   * - …/text
     - Název agendy
     - "Agenda"."název" (Agenda.name)
   * - …/platnostOd
     - Platnost agendy pro daný subjekt - od
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy od" (ActivityRole.ActivityRoleForSubject.agendaValidFrom) – vezme se z libovolné činnostních role pro stejný kód agendy (viz atribut níže cinnostniRole.platnostOd)
   * - …/platnostDo
     - Platnost agendy pro daný subjekt – do
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy do" (ActivityRole.ActivityRoleForSubject.agendaValidTo) – vezme se z libovolné činnostních role pro stejný kód agendy (viz atribut níže cinnostniRole.platnostDo)
   * - cinnostniRole
     - Seznam agendových činnostních rolí z RPP, které si daný subjekt vybral v rámci oznámení působnosti OVM v agendě.
     - "Subjekt"."Činnostní role" (Subject.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu
   * - …/item
     - Kód činnostní role
     - "Činnostní role"."kód" (ActivityRole.code)
   * - …/text
     - Název činnostní role
     - "Činnostní role"."název" (ActivityRole.name)
   * - …/agenda
     - Kód agendy
     - "Činnostní role"."Agenda"."kód" (ActivityRole.Agenda.code)
   * - …/platnostOd
     - Platnost činnostní role pro daný subjekt - od
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy od" (ActivityRole.ActivityRoleForSubject.agendaValidFrom)
   * - …/platnostDo
     - Platnost činnostní role pro daný subjekt - do
     - Činnostní role"."Činnostní role pro subjekt"."platnost agendy do" (ActivityRole.ActivityRoleForSubject.agendaValidTo)
   * - casPosledniZmeny
     - Datum a čas poslední změny v údajích subjektu.
     - čas poslední změny subjektu v historických tabulkách; :ref:`ws:common`


.. _ws:updatesubject:

UpdateSubject
-------------

Metoda UpdateSubject na základě požadavku ``UpdateSubjectRequest`` provede změnu údajů daného subjektu a v odpovědi ``UpdateSubjectResponse`` se vrací výsledek provedené akce.

.. list-table:: Popis atributů ``UpdateSubjectRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - name
     - Oficiální název subjektu
     - "Subjekt"."název" (Subject.name)
   * - typInstituce
     - Typ instituce
     - "Subjekt"."Typ instituce"."kód" (Subject.InstitutionType.code)
   * - contactAddress
     - Adresa
     - "Subjekt"."Kontakt"."Adresa" (Subject.Contact.Address) – vazba "adresa úřadu" (officeAddress); :ref:`ws:common`. 
   * - contactAddressPostalCode
     - Poštovní směrovací číslo přidělené pro účely úřadu
     - "Subjekt"."Kontakt"."psč úřadu" (Subject.Contact.officeZipCode)
   * - contactAddressPoBoxCode
     - Číslo poštovní přihrádky
     - "Subjekt"."Kontakt"."p.o. box úřadu" (Subject.Contact.officePoBox)
   * - deliveryAddress
     - Kontaktní poštovní adresa
     - "Subjekt"."Kontakt"."Adresa" (Subject.Contact.Address) - vazba "kontaktní poštovní adresa" (contactPostalAddress); :ref:`ws:common`
   * - deliveryAddressPostalCode
     - Poštovní směrovací číslo kontaktní poštovní adresy přidělené pro účely úřadu
     - "Subjekt"."Kontakt"."psč úřadu poštovní adresy" (Subject.Contact.postalAddressZipCode)
   * - deliveryAddressPoBoxCode
     - Číslo poštovní přihrádky kontaktní poštovní adresy
     - "Subjekt"."Kontakt"."p.o. box úřadu poštovní adresy" (Subject.Contact.postalAdressPoBox)
   * - email
     - Seznam kontaktních e-mailů
     - "Subjekt"."Kontakt"."Email" (Subject.Contact.Email); :ref:`ws:common:update`
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel
     - "Subjekt"."Kontakt"."Telefon" (Subject.Contact.PhoneNumber); :ref:`ws:common:update`
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - prijataPusobnostVolby
     - Seznam veřejnoprávních smluv s obcemi, které přenesly svoji působnost na subjekt.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „cílovým subjektem“ a kde „Typ působnosti“ = „Pro volby“
   * - …/subject
     - Zkratka obce (jiného subjektu), který přenesl svoji působnost na subjekt.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "zdrojový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - predanaPusobnostVolby
     - Seznam veřejnoprávních smluv s obcemi, na které subjekt přenesl svoji působnost.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „zdrojovým subjektem“ a kde „Typ působnosti“ = „Pro volby“
   * - …/subject
     - Zkratka obce (jiného subjektu), na který subjekt přenesl svoji působnost.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "cílový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - …/reason
     - Důvod předané působnosti.
     - "Působnost"."důvod" (Authority.reason)
   * - prijataPusobnostAdmin
     - Seznam veřejnoprávních smluv s obcemi, které přenesly svoji působnost na subjekt.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „cílovým subjektem“ a kde „Typ působnosti“ = „Lokální administrátor“
   * - …/subject
     - Zkratka obce (jiného subjektu), který přenesl svoji působnost na subjekt.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "zdrojový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - predanaPusobnostAdmin
     - Seznam veřejnoprávních smluv s obcemi, na které subjekt přenesl svoji působnost.
     - "Působnost" (Authority) pro ty působnosti, pro které je daný subjekt „zdrojovým subjektem“ a kde „Typ působnosti“ = „Lokální administrátor“
   * - …/subject
     - Zkratka obce (jiného subjektu), na který subjekt přenesl svoji působnost.
     - "Působnost"."Subjekt"."zkratka" (Authority.Subject.shortcut) takového subjektu, na nějž směřuje vazba "cílový subjekt"
   * - …/contract
     - Číslo uzavřené veřejnoprávní smlouvy.
     - "Působnost"."číslo smlouvy" (Authority.contractNumber)
   * - …/reason
     - Důvod předané působnosti.
     - "Působnost"."důvod" (Authority.reason)

     
.. _ws:getdataboxlist:

GetDataboxList
--------------

Metoda GetDataboxList na základě požadavku ``GetDataboxListRequest`` vrací v odpovědi ``GetSubjectResponse`` jednu hlavní datovou schránku daného subjektu.

.. admonition:: Příklad žádosti GetDataboxList
   :class: info

   .. literalinclude:: _static/xml/GetDataboxListRequest.xml
      :language: xml

.. admonition:: Příklad odpovědi GetDataboxListResponse
   :class: info

   .. literalinclude:: _static/xml/GetDataboxListResponse.xml
      :language: xml


.. list-table:: Popis atributů ``GetDataboxListResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - total
     - Celkový počet vrácených datových schránek.
       V případě velkého množství záznamů se vrací jen jejich část. Počáteční záznam pro stránkování je možné určit atributem "start".
     - Bude vždy 1, protože v CAAIS je jenom 1 hlavní DS synchronizovaná z ROS.
   * - object-id
     - ID datové schránky.
     - "Subjekt"."Datová schránka"."id datové schránky" (Subject.DataBox.dataBoxId)
   * - name
     - Adresa
     - "Subjekt"."název" (Subject.name)
   * - street
     - Ulice
     - "Subjekt"."Kontakt"."Adresa"."název ulice" (Subject.Contact.Address.streetName) – vazba ze subjektu "adresa úřadu" (officeAddress)
   * - houseNumber
     - Číslo domovní
     - <prázdná_hodnota> (neexistuje odpovídající atribut)
   * - sequenceNumber
     - Číslo orientační
     - <prázdná_hodnota> (neexistuje odpovídající atribut)
   * - town
     - Město - adresa
     - "Subjekt"."Kontakt"."Adresa"."název obce" (Subject.Contact.Address.municipality) – vazba ze subjektu "adresa úřadu" (officeAddress)
   * - isdsBoxCreateTime
     - Čas poslední změny datové schránky.
     - "Subjekt"."Datová schránka"." čas poslední změny " (Subject.DataBox. lastChangeTime)
   * - :bdg-primary:`WS 1.1` isdsBoxChangeTime
     - Datum a čas poslední změny v údajích datové schránky.
     - čas poslední změny datové schránky v historických tabulkách jako Unix timestamp v sekundách

      
Správa uživatelských profilů
============================

.. _ws:getuserlist:

GetUserList
-----------

Metoda GetUserList na základě požadavku ``GetUserListRequest`` vrací v odpovědi ``GetUserListResponse`` seznam uživatelů (uživatelských profilů) daného subjektu (plyne z URL endpointu). Pro jeden požadavek se vrací maximálně 500 záznamů.

.. admonition:: Příklad žádosti GetUserListRequest
   :class: info

   .. literalinclude:: _static/xml/GetUserListRequest.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserListRequest``
   :header-rows: 1

   * - Název
     - Popis
   * - start
     - Počáteční pozice záznamu, od kterého bude vrácen seznam záznamů. Používá se v případě velkého množství záznamů pro stránkování a výchozí hodnota je 1.
     
     
.. admonition:: Příklad odpovědi GetUserListResponse
   :class: info

   .. literalinclude:: _static/xml/GetUserListResponse.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserListResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - total
     - Celkový počet uživatelů. V případě velkého množství záznamů se vrací jen jejich část. Počáteční záznam pro stránkování je možné určit atributem "start".
     - Počet aktivních profilů pod daným subjektem. "Subjekt"."Profil".."Stav profilu" (Subject.Profile.ProfileState) = "Aktivní"
   * - object-id
     - Přihlašovací jméno uživatele.
     - "Profil"."uživatelské jméno" (Profile.loginName)
   * - isPrimaryPerson
     - Osoba je statutárním zástupcem orgánu veřejné moci.
     - "Profil"."statutární zástupce" (Profile.statutoryRepresentative)
   * - firstname
     - Křestní jméno
     - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
   * - surname
     - Příjmení
     - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
   * - loginDisabled
     - Příznak, zda je uživatelský účet zablokovaný.
     
       Poznámka: V CAAIS nelze uživatelské účty smazat, ale pouze zablokovat.
     - "Profil"."Stav profilu" (Profile.ProfileState)
     
       - "Aktivní" ⇒ "FALSE"
       - "Neaktivní" ⇒ "TRUE"
   * - userAllRole
     - Povolené role uživatele
     - *neexistuje* (v CAAIS se nespravují CzechPoint role v tomto elementu jinak vracené)
   * - verejnaOsoba
     - Příznak, zda se jedná o veřejnou osobu, tzn. může jí Seznam OVM zobrazit
     - "Profil"."veřejná osoba" (Profile.publicPerson)
   * - casPosledniZmeny
     - Datum a čas poslední změny údajů uživatele
     - čas poslední změny profilu v historických tabulkách jako Unix timestamp v sekundách



.. _ws:getuser:

GetUser
-------

Metoda GetUser na základě požadavku ``GetUserRequest`` vrací v odpovědi ``GetUserResponse`` detailní informace o uživateli (uživatelském profilu) z daného subjektu.

.. admonition:: Příklad žádosti GetUserRequest
   :class: info
   
   .. literalinclude:: _static/xml/GetUserRequest.xml
      :language: xml

.. list-table:: Popis atributů ``GetUserRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-id
     - Přihlašovací jméno uživatele.
     - "Profil"."uživatelské jméno" (Profile.loginName)


.. admonition:: Příklad odpovědi GetUserResponse
   :class: info
   
   .. literalinclude:: _static/xml/GetUserResponse.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserListResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - titulPred
     - Titul před jménem
     - "Profil"."Fyzická osoba"."titul před" (Profile.PhysicalPerson.degreeBefore)
   * - firstname
     - Křestní jméno
     - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
   * - surname
     - Příjmení
     - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
   * - titulZa
     - Titul za jménem
     - "Profil"."Fyzická osoba"."titul za" (Profile.PhysicalPerson.degreeAfter)
   * - photo
     - Fotografie uživatele
     - "Fyzická osoba"."fotografie" (PhysicalPerson.photo)
   * - loginDisabled
     - Příznak, zda je uživatelský účet zablokovaný.
       Poznámka: V CAAIS nelze uživatelské účty smazat, ale pouze zablokovat.
     - "Profil"."Stav profilu" (Profile.ProfileState)
     
       - "Aktivní" ⇒ "FALSE"
       - "Neaktivní" ⇒ "TRUE"
   * - :bdg-primary:`WS 1.1` isPrimaryPerson
     - Značí, že je uživatel statutární zástupce daného subjektu.
     - "Profil"."statutární zástupce" (Profile.statutoryRepresentative)
   * - :bdg-primary:`WS 1.1` identifiedByROB
     - Značí, že byl uživatel ztotožněn (nalezeno AIFO v ROB).
     - "Profil"."Fyzická osoba"."osoba evidována v rob" (Profile.PhysicalPerson.personInRob)
   * - address
     - Adresa (viz společné typy).
     - Soukromá adresa se v CAAIS u uživatele neukládá, dotahuje se tedy adresa ze subjektu pod, kterým je daný profil.
     
       "Subjekt"."Kontakt"."Adresa" (Subject.Contact.Address) – vazba "adresa úřadu" (officeAddress)
   * - email
     - Seznam e-mailů.
     - Email pro profil je pouze jeden
   * - …/type
     - Kód typu emailu
     - = 1 (výchozí typ)
   * - …/text
     - Název typu emailu
     - = "oficiální" (výchozí typ)
   * - …/email
     - Emailová adresa
     - "Profil"."email" (Profile.email)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel
     - "Profil"."Telefon" (Profile.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/text
     - Název typu telefonu
     - "Telefon"."Typ Telefonu"."název" (PhoneNumber.PhoneNumberType.name)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - clientCertificate
     - Seznam certifikátů uživatele
     - = "Uživatel"."Certifikát X509" (User. X509Certificate), pokud již uživatel existuje v CAAIS-IdP = Certifikát v pomocné tabulky "Certifikát pro samoztotožnění", pokud ještě uživatel není uložen v CAAIS-IdP.
   * - …/type
     - Kód typu certifikátu
     
       - V – komerční
       - Q – kvalifikovaný
     - = "Certifikát X509"."Typ certifikátu"."kód" (X509Certificate.CertificateType.code), pokud již uživatel existuje v CAAIS-IdP. Jinak
       = Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
   * - …/text
     - Název typu certifikátu
     - = "Certifikát X509"."Typ certifikátu"."název" (X509Certificate.CertificateType.name), pokud již uživatel existuje v CAAIS-IdP. Jinak
       = Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
   * - …/number
     - Sériové číslo certifikátu v dekadickém nebo hexadecimálním tvaru.
     - = "Certifikát X509"."sériové číslo" (X509Certificate.serialNumber), pokud již uživatel existuje v CAAIS-IdP. Jinak
       = Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
   * - …/issuer
     - Řetězec pro označení vydavatele certifikátu
     - = "Certifikát X509"."certifikační autorita" (X509Certificate.certificateAuthority), pokud již uživatel existuje v CAAIS-IdP. Jinak
       = Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
   * - aisRole
     - Seznam rolí pro přístup do aplikací
     - "Profil"."Přístupová role" (Profile.AccessRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu
       Pokud má profil přiřazeny Skupiny rolí nebo Business role dotahují se přes ně odpovídající přístupové role. Dále se dotahují i delegované přístupové role přes "Vazební profil".
       Hodnota atributu je ve formátu: <zkratka_ais>.<zkratka_pristupove_role>
       Příklad: testAis1.testRole1
   * - …/item
     - Zkratka role
     - "Přístupová role"."zkratka" (AccessRole.shortcut)
   * - …/text
     - Název role
     - "Přístupová role"."název" (AccessRole.name)
   * - function
     - Funkce osoby
     - "Profil"."funkce" (Profile.function)
   * - verejnaOsoba
     - Příznak, zda se jedná o veřejnou osobu, tzn. může jí Seznam OVM zobrazit
     - "Profil"."veřejná osoba" (Profile.publicPerson)
   * - poznamka
     - Poznámka
     - "Fyzická osoba"."poznámka" (PhysicalPerson.note)
   * - agendy
     - Agendy činnostních rolí přiřazených uživateli
     - "Profil"."Činnostní role"."Agenda" (Profile.ActivityRole.Agenda) – pouze ty agendy, jejichž činnostní role jsou aktivní a mají aktivní přiřazení subjektu
       Pokud má profil přiřazeny Skupiny rolí nebo Business role dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".
   * - …/item
     - Kód agendy
     - "Agenda"."kód" (Agenda.code)
   * - …/text
     - Název agendy
     - "Agenda"."název" (Agenda.name)
   * - …/platnostOd
     - Platnost agendy pro daný subjekt – od
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy od" (ActivityRole.ActivityRoleForSubject.agendaValidFrom) – vezme se z libovolné činnostních role pro stejný kód agendy (viz atribut níže cinnostniRole.platnostOd)
   * - …/platnostDo
     - Platnost agendy pro daný subjekt – do
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy do" (ActivityRole.ActivityRoleForSubject.agendaValidTo) – vezme se z libovolné činnostních role pro stejný kód agendy (viz atribut níže cinnostniRole.platnostDo)
   * - cinnostniRole
     - Agendové činnostní role přiřazené uživateli.
     - "Profil"."Činnostní role" (Profile.ActivityRole) – pouze ty, které jsou aktivní a mají aktivní přiřazení subjektu
       Pokud má profil přiřazeny Skupiny rolí nebo Business role dotahují se přes ně odpovídající činnostní role a agendy. Dále se dotahují i delegované činnostní role a agendy přes "Vazební profil".
   * - …/item
     - Kód činnostní role
     - "Činnostní role"."kód" (ActivityRole.code)
   * - …/text
     - Název činnostní role
     - "Činnostní role"."název" (ActivityRole.name)
   * - …/platnostOd
     - Platnost činnostní role pro daný subjekt – od
     - "Činnostní role"."Činnostní role pro subjekt"."platnost agendy od" (ActivityRole.ActivityRoleForSubject.agendaValidFrom)
   * - …/platnostDo
     - Platnost činnostní role pro daný subjekt – do
     - Činnostní role"."Činnostní role pro subjekt"."platnost agendy do" (ActivityRole.ActivityRoleForSubject.agendaValidTo)
   * - casPosledniZmeny
     - Datum a čas poslední změny v údajích uživatele
     - čas poslední změny profilu v historických tabulkách


.. _ws:createuser:

CreateUser
----------

Metoda CreateUser na základě požadavku ``CreateUserRequest`` vytvoří nového uživatele (uživatelský profil) v definovaném stavu dle atributu ``loginDisabled`` v požadavku (může být „aktivní“ nebo „neaktivní“) a zároveň FO ve stavu „před ztotožněním“ a s parametrem „osoba evidována v ROB“ (personInRob) = „Ne“ pod daným subjektem a v odpovědi ``CreateUserResponse`` se vrací výsledek provedené akce. Vzhledem k tomu, že CAAIS vyžaduje při založení nového uživatelského profilu také ztotožnění FO (přidělení AIFO), je po založení profilu odeslána žádost o ztotožnění na zadaný uživatelský e-mail. Až po provedení tohoto ztotožnění je v CAAIS založena platná fyzická osoba a je možné se následně pomocí CAAIS-IdP autentizovat.

.. dropdown:: CAAIS Internals
   :color: muted
   :icon: gear
   
   V systému CAAIS se provádí následující kroky:
     - založení FO ve stavu „Před ztotožněním“ a parametrem „Osoba evidována v ROB“ (personInRob) = „Ne“
     - založení Profilu ve stavu dle požadavku („Aktivní“ nebo „Neaktivní“)
     - uložení seznamu certifikátů do pomocné technické tabulky „Certifikát pro samoztotožnění“
     - odeslání emailu uživateli s odkazem na stránku pro samoztotožnění

Předání dat do CAAIS-IdP se v tuto chvíli ještě neprovádí, to se provádí právě až v metodě :ref:`ws:identifyagainstrob` nebo při samoztotožnění uživatelem.

Metodu je možné volat s prázdným atributem ``object-id``. V takovém případě CAAIS vygeneruje jméno profilu (uživatelské jméno) ve tvaru „jmeno_prijmeni“, respektive „jmeno_prijmeni_#“, kde „#“ je číselný rozlišovač, je-li základní tvar již obsazen. Vygenerované jméno profilu se vrací v odpovědi jako atribut ``object-id``.

.. admonition:: Příklad žádosti CreateUserRequest
   :class: info
   
   .. literalinclude:: _static/xml/CreateUserRequest.xml
      :language: xml


.. list-table:: Popis atributů ``CreateUserRequest``
    :header-rows: 1

    * - Název
      - Popis
      - Atribut z datového modelu
    * - object-id
      - Jméno profilu / přihlašovací jméno uživatele.
      - "Profil"."uživatelské jméno" (Profile.loginName)
    * - titulPred
      - Titul před jménem
      - "Profil"."Fyzická osoba"."titul před" (Profile.PhysicalPerson.degreeBefore)
    * - firstname
      - Křestní jméno
      - "Profil"."Fyzická osoba"."jméno" (Profile.PhysicalPerson.firstName)
    * - surname
      - Příjmení
      - "Profil"."Fyzická osoba"."příjmení" (Profile.PhysicalPerson.lastName)
    * - titulZa
      - Titul za jménem
      - "Profil"."Fyzická osoba"."titul za" (Profile.PhysicalPerson.degreeAfter)
    * - password
      - Heslo
      - neukládá se (neexistuje odpovídající atribut, heslo v CAAIS-IdP si uživatel nastavuje sám zvlášť)
    * - photo
      - Fotografie uživatele
      - "Fyzická osoba"."fotografie" (PhysicalPerson.photo)
    * - loginDisabled
      - Příznak, zda je uživatelský účet zablokovaný.
        Poznámka: V CAAIS nelze uživatelské účty smazat, ale pouze zablokovat.
      - "Profil"."Stav profilu" (Profile.ProfileState)
      
        - "Aktivní" ⇒ "FALSE"
        - "Neaktivní" ⇒ "TRUE"
    * - email
      - Seznam e-mailů.
      - Email pro profil je pouze jeden a v seznamu emailů z požadavku se bere jen první s "type" = "1" (jedná se o typ "oficiální"), ostatní se ignorují. 
    * - …/type
      - Kód typu emailu
      - = 1 (výchozí typ); neukládá se (neexistuje odpovídající atribut)
    * - …/email
      - Emailová adresa
      - "Profil"."email" (Profile.email)
    * - telephoneNumber
      - Seznam kontaktních telefonních čísel
      - "Profil"."Telefon" (Profile.PhoneNumber)
    * - …/type
      - Kód typu telefonu
      - "Telefon"."Typ Telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
    * - …/number
      - Telefonní číslo
      - "Telefon"."hodnota" (PhoneNumber.value)
    * - clientCertificate
      - Seznam certifikátů uživatele.
      - Certifikát v pomocné tabulky "Certifikát pro samoztotožnění". Ukládá se jen typ certifikátu "V" (Komerční), ostatní typy se ignorují.
    * - …/type
      - Kód typu certifikátu
     
        - V – komerční
        - Q – kvalifikovaný
      -  Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
    * - …/number
      - Sériové číslo certifikátu v dekadickém nebo hexadecimálním tvaru.
      - Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
    * - …/issuer
      - Řetězec pro označení vydavatele certifikátu
      - Odpovídající atribut v tabulce "Certifikát pro samoztotožnění".
    * - aisRole
      - Seznam rolí pro přístup do aplikací, které mají být přiřazeny uživateli.
      - "Profil"."Přístupová role" (Profile.AccessRole)
        
        Role se přiřadí k profilu jen tehdy, pokud je role aktivní a má aktivní přiřazení subjektu.
         
        Hodnota atributu je ve formátu: <zkratka_ais>.<zkratka_pristupove_role>
        Příklad: testAis1.testRole1
    * - …/item
      - Zkratka role
      - "Přístupová role"."zkratka" (AccessRole.shortcut)
    * - cinnostniRole
      - Seznam agendových činnostních rolí, které mají být přiřazeny uživateli.
      - "Profil"."Činnostní role" (Profile.ActivityRole)
      
        Role se přiřadí k profilu jen tehdy, pokud je role aktivní a má aktivní přiřazení subjektu.
    * - …/item
      - Kód činnostní role
      - "Činnostní role"."kód" (ActivityRole.code)
    * - function
      - Funkce osoby.
      - "Profil"."funkce" (Profile.function)
    * - verejnaOsoba
      - Příznak, zda se jedná o veřejnou osobu, tzn. může jí Seznam OVM zobrazit.
      - "Profil"."veřejná osoba" (Profile.publicPerson)
    * - poznamka
      - Poznámka
      - "Fyzická osoba"."poznámka" (PhysicalPerson.note)

      
.. admonition:: Příklad odpovědi CreateUserResponse
   :class: info
   
   .. literalinclude:: _static/xml/CreateUserResponse.xml
      :language: xml


.. list-table:: Popis atributů ``CreateUserRequest``
    :header-rows: 1

    * - Název
      - Popis
      - Atribut z datového modelu
    * - object-id
      - Jméno vytvořeného profilu / přihlašovací jméno uživatele.
      - "Profil"."uživatelské jméno" (Profile.loginName).


.. _ws:updateuser:

UpdateUser
----------

Metoda UpdateUser na základě požadavku ``UpdateUserRequest`` provede změnu údajů uživatele (uživatelského profilu) pod daným subjektem a v odpovědi ``UpdateUserResponse`` se vrací výsledek provedené akce. Metoda používá stejné elementy jako ``CreateUserRequest``. Uvádí se jen ty elementy, jejichž hodnoty se mění; atribut ``object-id`` je povinný a identifikuje měněný profil.

Množinové elementy (například seznam telefonních čísel či seznam přístupových rolí) se nastavují vždy jako celá množina, nikoli změnově. Je-li *N* nastavovaná množina a *P* původní množina, pak prvky v rozdílu *N* ∖ *P* jsou přidány a prvky v rozdílu *P* ∖ *N* odebrány. V případě přístupových rolí (``aisRole``) jest lze takto měnit přístupové role pouze přiřazené přímo profilu, nikoli přístupové role přiřazené nepřímo prostřednictvím skupiny rolí a organizačních rolí. (Metoda ``GetUserRequest`` vrací v seznamu přístupových rolí i role přiřazené nepřímo, které zde nelze odebrat.)

Uživatele (uživatelský profil) není možné smazat, pouze se pomocí atributu ``loginDisabled`` může zablokovat (deaktivovat). U osob ztotožněných vůči ROB nelze měnit jméno a příjmení – služba v takovém případě vrátí chybu. 

.. admonition:: Příklad žádosti UpdateUserRequest
   :class: info
   
   .. literalinclude:: _static/xml/UpdateUserRequest.xml
      :language: xml

.. admonition:: Příklad odpovědi UpdateUserResponse
   :class: info
   
   .. literalinclude:: _static/xml/UpdateUserResponse.xml
      :language: xml


Správa zřizovaných organizací
=============================

.. _ws:getorganizationlist:

GetOrganizationList
-------------------

Metoda GetOrganizationList na základě požadavku ``GetOrganizationListRequest`` vrací v odpovědi ``GetOrganizationListResponse`` seznam zřizovaných organizací daného subjektu. Pro jeden požadavek se vrací maximálně 500 záznamů.

.. admonition:: Příklad žádosti GetOrganizationListRequest
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationListRequest.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserOrganizationListRequest``
   :header-rows: 1

   * - Název
     - Popis
   * - start
     - Počáteční pozice záznamu, od kterého bude vrácen seznam záznamů. Používá se v případě velkého množství záznamů pro stránkování a výchozí hodnota je 1.
     
     
.. admonition:: Příklad odpovědi GetOrganizationListResponse
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationListResponse.xml
      :language: xml
      

.. list-table:: Popis atributů ``GetOrganizationListResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - total
     - Celkový počet zřizovaných organizací.
       
       V případě velkého množství záznamů se vrací jen jejich část. Počáteční záznam pro stránkování je možné určit atributem "start".
     - Počet zřizovaných organizací "Subjekt"."Zřizovaná organizace" (Subject.Organization)
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)
   * - name
     - Název zřizované organizace.
     - "Zřizovaná organizace"."název" (Organization.name)
   * - :bdg-primary:`WS 1.1` casPosledniZmeny
     - Datum a čas poslední změny v údajích zřizované organizace.
     - Čas poslední změny zřizované organizace v historických tabulkách jako Unix timestamp v sekundách
   
.. _ws:getorganization:

GetOrganization
---------------

Metoda GetOrganization na základě požadavku ``GetOrganizationRequest`` vrací v odpovědi ``GetOrganizationResponse`` údaje zřizované organizace pod daným subjektem.

.. admonition:: Příklad žádosti GetOrganizationRequest
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationRequest.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserOrganizationRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)
 
.. admonition:: Příklad odpovědi GetOrganizationResponse
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationResponse.xml
      :language: xml
      

.. list-table:: Popis atributů ``GetOrganizationResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - name
     - Název zřizované organizace.
     - "Zřizovaná organizace"."název" (Organization.name)
   * - contactAddress
     - Adresa. 
     - "Zřizovaná organizace"."Adresa" (Organization.Address) – vazba "adresa zřizované organizace" (organizationAddress); :ref:`ws:common`.
   * - deliveryAddress
     - Kontaktní poštovní adresa. 
     - "Zřizovaná organizace"."Adresa" (Organization.Address) – vazba "poštovní adresa zřizované organizace" (deliveryAddress); :ref:`ws:common`.
   * - email
     - Seznam kontaktních e-mailů.
     - "Zřizovaná organizace"."Email" (Organization.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/text
     - Název typu emailu
     - "Email"."Typ emailu"."název" (Email.EmailType.name)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel.
     - "Zřizovaná organizace"."Telefon" (Organization.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/text
     - Název typu telefonu
     - "Telefon"."Typ telefonu"."název" (PhoneNumber.PhoneNumberType.name)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - ico
     - IČ organizace.
     - "Zřizovaná organizace"."ič" (Organization.identificationNumber)
   * - dic
     - DIČ 
     - "Zřizovaná organizace"."dič" (Organization.vatId)
   * - typOrganizace
     - Typ zřizované organizace.
     - "Zřizovaná organizace"."Typ organizace"."kód" (Organization.OrganizationType.code)
   * - …/text
     - Název typu zřizované organizace
     - "Zřizovaná organizace"."Typ organizace"."název" (Organization.OrganizationType.name)
   * - bankAccount
     - Bankovní spojení. Obsahuje 4-číselný kód banky a číslo účtu.
     - "Zřizovaná organizace"."Bankovní spojení" (Organization.BankAccount)
   * - …/number
     - Číslo účtu
     - "Bankovní spojení"."číslo účtu" (BankAccount.number)
   * - …/bankCode
     - Kód banky
     - "Bankovní spojení"."kód banky" (BankAccount.bankCode)
   * - …/description
     - Popis
     - "Bankovní spojení"."popis" (BankAccount.description)
   * - officesHours
     - Úřední hodiny obsahují den v týdnu (1 pondělí – 7 neděle) a čas (hodinu a minutu ve tvaru HH:MM) začátku a konce úředních hodin. V případě přestávky zadejte den dvakrát (s dopoledním a poté s odpoledním časovým intervalem)
     - "Zřizovaná organizace"."Úřední hodiny zřizované organizace" (Organization.OrganizationOfficeHours)
   * - …/day
     - Den v týdnu
     - "Úřední hodiny zřizované organizace"."den v týdnu" (OrganizationOfficeHours.day)
   * - …/from
     - Od
     - "Úřední hodiny zřizované organizace"."od" (OrganizationOfficeHours.from)
   * - …/to
     - Do
     - "Úřední hodiny zřizované organizace"."do" (OrganizationOfficeHours.to)
   * - subjectCode
     - Číslo subjektu, kód ČSU.
     - "Zřizovaná organizace"."číslo subjektu" (Organization.subjectCode)
   * - url
     - WWW odkaz
     - "Zřizovaná organizace"."Url WWW" (Organization.WwwUrl)
   * - …/url
     - URL adresa
     - "Url WWW"."url" (WwwUrl.url)
   * - …/description
     - Poznámka
     - "Url WWW"."poznámka" (WwwUrl.note)
   * - …/type
     - Kód typu URL
     - "Url WWW"."Typ Url WWW"."kód" (WwwUrl.WwwUrlType.code)
   * - …/text
     - Název typu URL
     - "Url WWW"."Typ Url WWW"."název" (WwwUrl.WwwUrlType.name)
   * - roleCentralniNakup
     - Seznam rolí pro přístup do aplikace Centrální nákup.
     - "Zřizovaná organizace"."Role centrálního nákupu zřizované organizace" (Organization. OrganizationCentralPurchaseRole)
   * - …/item
     - ID role
     - "Role centrálního nákupu zřizované organizace"."kód" (OrganizationCentralPurchaseRole.code)
   * - …/text
     - Název role
     - "Role centrálního nákupu zřizované organizace"."název" (OrganizationCentralPurchaseRole.name)
   * - zruseno
     - Značí, že organizace byla zrušena.
     - = "Ano", pokud je vyplněn atribut "Zřizovaná organizace"."čas zrušení" (Organization.cancelationTime) <= aktuální datum
     
       = "Ne", pokud není vyplněn atribut "Zřizovaná organizace"."čas zrušení" (Organization.cancelationTime) nebo je > aktuální datum
   * - casZruseni
     - Čas zrušení organizace.
     - "Zřizovaná organizace"."čas zrušení" (Organization.cancelationTime)
   * - :bdg-primary:`WS 1.1` casPosledniZmeny
     - Datum a čas poslední změny v údajích zřizované organizace.
     - Čas poslední změny zřizované organizace v historických tabulkách jako Unix timestamp v sekundách

 
 
.. _ws:createorganization:

CreateOrganization
------------------

Metoda CreateOrganization na základě požadavku ``CreateOrganizationRequest`` vytvoří novou zřizovanou organizaci pod daným subjektem a v odpovědi ``CreateOrganizationResponse`` se vrací výsledek provedené akce.

.. admonition:: Příklad žádosti CreateOrganizationRequest
   :class: info

   .. literalinclude:: _static/xml/CreateOrganizationRequest.xml
      :language: xml


.. list-table:: Popis atributů ``CreateOrganizationResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - name
     - Název zřizované organizace.
     - "Zřizovaná organizace"."název" (Organization.name)
   * - contactAddress
     - Adresa. 
     - "Zřizovaná organizace"."Adresa" (Organization.Address) – vazba "adresa zřizované organizace" (organizationAddress); :ref:`ws:common`.
   * - deliveryAddress
     - Kontaktní poštovní adresa. 
     - "Zřizovaná organizace"."Adresa" (Organization.Address) – vazba "poštovní adresa zřizované organizace" (deliveryAddress); :ref:`ws:common`.
   * - email
     - Seznam kontaktních e-mailů.
     - "Zřizovaná organizace"."Email" (Organization.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel.
     - "Zřizovaná organizace"."Telefon" (Organization.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - ico
     - IČ organizace.
     - "Zřizovaná organizace"."ič" (Organization.identificationNumber)
   * - dic
     - DIČ 
     - "Zřizovaná organizace"."dič" (Organization.vatId)
   * - typOrganizace
     - Typ zřizované organizace.
     - "Zřizovaná organizace"."Typ organizace"."kód" (Organization.OrganizationType.code)
   * - bankAccount
     - Bankovní spojení. Obsahuje 4-číselný kód banky a číslo účtu.
     - "Zřizovaná organizace"."Bankovní spojení" (Organization.BankAccount)
   * - …/number
     - Číslo účtu
     - "Bankovní spojení"."číslo účtu" (BankAccount.number)
   * - …/bankCode
     - Kód banky
     - "Bankovní spojení"."kód banky" (BankAccount.bankCode)
   * - …/description
     - Popis
     - "Bankovní spojení"."popis" (BankAccount.description)
   * - officesHours
     - Úřední hodiny obsahují den v týdnu (1 pondělí – 7 neděle) a čas (hodinu a minutu ve tvaru HH:MM) začátku a konce úředních hodin. V případě přestávky zadejte den dvakrát (s dopoledním a poté s odpoledním časovým intervalem)
     - "Zřizovaná organizace"."Úřední hodiny zřizované organizace" (Organization.OrganizationOfficeHours)
   * - …/day
     - Den v týdnu
     - "Úřední hodiny zřizované organizace"."den v týdnu" (OrganizationOfficeHours.day)
   * - …/from
     - Od
     - "Úřední hodiny zřizované organizace"."od" (OrganizationOfficeHours.from)
   * - …/to
     - Do
     - "Úřední hodiny zřizované organizace"."do" (OrganizationOfficeHours.to)
   * - subjectCode
     - Číslo subjektu, kód ČSU.
     - "Zřizovaná organizace"."číslo subjektu" (Organization.subjectCode)
   * - url
     - WWW odkaz
     - "Zřizovaná organizace"."Url WWW" (Organization.WwwUrl)
   * - …/url
     - URL adresa
     - "Url WWW"."url" (WwwUrl.url)
   * - …/description
     - Poznámka
     - "Url WWW"."poznámka" (WwwUrl.note)
   * - …/type
     - Kód typu URL
     - "Url WWW"."Typ Url WWW"."kód" (WwwUrl.WwwUrlType.code)
   * - roleCentralniNakup
     - Seznam rolí pro přístup do aplikace Centrální nákup.
     - "Zřizovaná organizace"."Role centrálního nákupu zřizované organizace" (Organization. OrganizationCentralPurchaseRole)
   * - …/item
     - ID role
     - "Role centrálního nákupu zřizované organizace"."kód" (OrganizationCentralPurchaseRole.code)
   * - zruseno
     - Značí, že organizace byla zrušena.
     - vyplní se atribut "Zřizovaná organizace"."čas zrušení" (Organization.cancelationTime) = aktuální datum, pokud TRUE
     
.. admonition:: Příklad odpovědi CreateOrganizationResponse
   :class: info

   .. literalinclude:: _static/xml/CreateOrganizationResponse.xml
      :language: xml

.. list-table:: Popis atributů ``CreateOrganizationResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-id
     - ID (zkratka) nové zřizované organizace vygenerované ze zadaného atributu "name".
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)


.. _ws:updateorganization:

UpdateOrganization
------------------

Metoda UpdateOrganization na základě požadavku ``UpdateOrganizationRequest`` provede změnu údajů zřizované organizace pod daným subjektem a v odpovědi ``UpdateOrganizationResponse`` se vrací výsledek provedené akce. Metoda používá stejné elementy jako ``CreateOrganizationRequest``. Uvádí se jen ty elementy, jejichž hodnoty se mění; atribut ``object-path`` je povinný a identifikuje měněnou organizaci.

.. admonition:: Příklad žádosti UpdateOrganizationRequest
   :class: info

   .. literalinclude:: _static/xml/UpdateOrganizationRequest.xml
      :language: xml

.. admonition:: Příklad odpovědi UpdateOrganizationResponse
   :class: info

   .. literalinclude:: _static/xml/UpdateOrganizationResponse.xml
      :language: xml


Správa uživatelů zřizovaných organizací
=======================================

.. _ws:getorganizationuserlist:

GetOrganizationUserList
-----------------------

Metoda GetOrganizationUserList na základě požadavku ``GetOrganizationUserListRequest`` vrací v odpovědi ``GetOrganizationUserListResponse`` seznam uživatelů zřizované organizace daného subjektu. Pro jeden požadavek se vrací maximálně 500 záznamů.

.. admonition:: Příklad žádosti GetOrganizationUserListRequest
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationUserListRequest.xml
      :language: xml


.. list-table:: Popis atributů ``GetUserOrganizationUserListRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - start
     - Počáteční pozice záznamu, od kterého bude vrácen seznam záznamů. Používá se v případě velkého množství záznamů pro stránkování a výchozí hodnota je 1.
     -
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)
     
     
.. admonition:: Příklad odpovědi GetOrganizationUserListResponse
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationUserListResponse.xml
      :language: xml
      

.. list-table:: Popis atributů ``GetOrganizationUserListResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - total
     - Celkový počet uživatelů zřizované organizace.
     
       V případě velkého množství záznamů se vrací jen jejich část. Počáteční záznam pro stránkování je možné určit atributem "start".
     - Počet uživatelů zřizované organizace "Subjekt"."Zřizovaná organizace"."Uživatel zřizované organizace" (Subject.Organization. OrganizationUser)
   * - object-id
     - Přihlašovací jméno uživatele.
     - "Uživatel zřizované organizace"."přihlašovací jméno" (OrganizationUser.loginName)
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)
   * - firstname
     - Křestní jméno.
     - "Uživatel zřizované organizace"."jméno" (OrganizationUser.firstname)
   * - surname
     - Příjmení.
     - "Uživatel zřizované organizace"."příjmení" (OrganizationUser.surname)
   * - :bdg-primary:`WS 1.1` loginDisabled
     - Příznak, zda je uživatelský účet zablokovaný.
       
       Poznámka: V CAAIS nelze uživatelské účty smazat, ale pouze zablokovat.
     - "Uživatel zřizované organizace"."účet zablokován" (OrganizationUser.loginDisabled)
   * - email
     - Seznam e-mailů.
     - "Uživatel zřizované organizace"."Email"  (OrganizationUser.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/text
     - Název typu emailu
     - "Email"."Typ emailu"."název" (Email.EmailType.name)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - uvolnenZeZamestnani
     - Příznak, je-li osoba uvolněna z předchozího zaměstnání pro výkon funkce.
     - "Uživatel zřizované organizace"."uvolněn ze zaměstnání" (OrganizationUser.employmentDismissed)
   * - :bdg-primary:`WS 1.1` casPosledniZmeny
     - Datum a čas poslední změny v údajích uživatele zřizované organizace.
     - Čas poslední změny uživatele zřizované organizace v historických tabulkách jako Unix timestamp v sekundách

     
.. _ws:getorganizationuser:

GetOrganizationUser
-------------------

Metoda GetOrganizationUser na základě požadavku GetOrganizationUserRequest vrací v odpovědi GetOrganizationUserResponse údaje uživatele zřizované organizace pod daným subjektem.


.. admonition:: Příklad žádosti GetOrganizationUserRequest
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationUserRequest.xml
      :language: xml

.. list-table:: Popis atributů ``GetUserOrganizationUserRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-id
     - Přihlašovací jméno uživatele.
     - "Uživatel zřizované organizace"."přihlašovací jméno" (OrganizationUser.loginName)
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)

     
.. admonition:: Příklad odpovědi GetOrganizationUserResponse
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationUserResponse.xml
      :language: xml
      

.. list-table:: Popis atributů ``GetOrganizationUserResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - titulPred
     - Titul před jménem.
     - "Uživatel zřizované organizace"."titul před" (OrganizationUser.degreeBefore)
   * - firstname
     - Křestní jméno.
     - "Uživatel zřizované organizace"."jméno" (OrganizationUser.firstname)
   * - surname
     - Příjmení.
     - "Uživatel zřizované organizace"."příjmení" (OrganizationUser.surname)
   * - titulZa
     - Titul za jménem.
     - "Uživatel zřizované organizace"."titul za" (OrganizationUser.degreeAfter)
   * - :bdg-primary:`WS 1.1` identifiedByROB
     - Značí, že byl uživatel ztotožněn (nalezeno AIFO v ROB).
     - <prázdná_hodnota> (neexistuje odpovídající atribut)
   * - photo
     - Fotografie uživatele.
     - "Uživatel zřizované organizace"."fotografie" (OrganizationUser.photo)
   * - loginDisabled
     - Příznak, že účet uživatele je zablokován.
     - "Uživatel zřizované organizace"."účet zablokován" (OrganizationUser.loginDisabled)
   * - address
     - Adresa. 
     - "Uživatel zřizované organizace"."Adresa" (OrganizationUser.Address); :ref:`ws:common`.
   * - email
     - Seznam e-mailů.
     - "Uživatel zřizované organizace"."Email" (OrganizationUser.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/text
     - Název typu emailu
     - "Email"."Typ emailu"."název" (Email.EmailType.name)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel.
     - "Uživatel zřizované organizace"."Telefon"  (OrganizationUser.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/text
     - Název typu telefonu
     - "Telefon"."Typ telefonu"."název" (PhoneNumber.PhoneNumberType.name)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - uvolnenZeZamestnani
     - Příznak, je-li osoba uvolněna z předchozího zaměstnání pro výkon funkce.
     - "Uživatel zřizované organizace"."uvolněn ze zaměstnání" (OrganizationUser.employmentDismissed)
   * - roleCentralniNakup
     - Seznam rolí pro přístup do aplikace Centrální nákup.
     - "Uživatel zřizované organizace"."Role centrálního nákupu zřizované organizace" (OrganizationUser. OrganizationCentralPurchaseRole)
   * - …/item
     - ID role
     - "Role centrálního nákupu zřizované organizace"."kód" (OrganizationCentralPurchaseRole.code)
   * - …/text
     - Název role
     - "Role centrálního nákupu zřizované organizace"."název" (OrganizationCentralPurchaseRole.name)
   * - :bdg-primary:`WS 1.1` casPosledniZmeny
     - Datum a čas poslední změny v údajích uživatelského účtu.
     - čas poslední změny uživatele zřizované organizace v historických tabulkách

     
.. _ws:createorganizationuser:

CreateOrganizationUser
----------------------

Metoda CreateOrganizationUser na základě požadavku ``CreateOrganizationUserRequest`` vytvoří nového uživatele zřizované organizace pod daným subjektem a v odpovědi ``CreateOrganizationUserResponse`` se vrací výsledek provedené akce.

Pro uživatele zřizované organizace se neprovádí ztotožňování jako pro standardního uživatele CAAIS.

.. admonition:: Příklad žádosti CreateOrganizationUserRequest
   :class: info

   .. literalinclude:: _static/xml/GetOrganizationUserRequest.xml
      :language: xml

.. list-table:: Popis atributů ``CreateUserOrganizationUserRequest``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-id
     - Přihlašovací jméno uživatele.
     - "Uživatel zřizované organizace"."přihlašovací jméno" (OrganizationUser.loginName)
   * - object-path
     - Zkratka zřizované organizace.
     - "Zřizovaná organizace"."zkratka" (Organization.shortcut)
   * - titulPred
     - Titul před jménem.
     - "Uživatel zřizované organizace"."titul před" (OrganizationUser.degreeBefore)
   * - firstname
     - Křestní jméno.
     - "Uživatel zřizované organizace"."jméno" (OrganizationUser.firstname)
   * - surname
     - Příjmení.
     - "Uživatel zřizované organizace"."příjmení" (OrganizationUser.surname)
   * - titulZa
     - Titul za jménem.
     - "Uživatel zřizované organizace"."titul za" (OrganizationUser.degreeAfter)
   * - photo
     - Fotografie uživatele.
     - "Uživatel zřizované organizace"."fotografie" (OrganizationUser.photo)
   * - loginDisabled
     - Příznak, že účet uživatele je zablokován.
     - "Uživatel zřizované organizace"."účet zablokován" (OrganizationUser.loginDisabled)
   * - address
     - Adresa. Pokud je zadán kód adresy, adresa je ověřena a doplněna z registru RUIAN. Není-li kód zadán, adresa se neověřuje a je považována za dočasnou
     - "Uživatel zřizované organizace"."Adresa" (OrganizationUser.Address); :ref:`ws:common`.

       Pro adresu bez kódu adresy se validuje povinné vyplnění těchto atributů:
       - houseNumber
       - cityCode
       - postalCode
   * - email
     - Seznam e-mailů.
     - "Uživatel zřizované organizace"."Email" (OrganizationUser.Email)
   * - …/type
     - Kód typu emailu
     - "Email"."Typ emailu"."kód" (Email.EmailType.code)
   * - …/email
     - Emailová adresa
     - "Email"."adresa" (Email.address)
   * - …/description
     - Poznámka
     - "Email"."poznámka" (Email.note)
   * - telephoneNumber
     - Seznam kontaktních telefonních čísel.
     - "Uživatel zřizované organizace"."Telefon"  (OrganizationUser.PhoneNumber)
   * - …/type
     - Kód typu telefonu
     - "Telefon"."Typ telefonu"."kód" (PhoneNumber.PhoneNumberType.code)
   * - …/number
     - Telefonní číslo
     - "Telefon"."hodnota" (PhoneNumber.value)
   * - uvolnenZeZamestnani
     - Příznak, je-li osoba uvolněna z předchozího zaměstnání pro výkon funkce.
     - "Uživatel zřizované organizace"."uvolněn ze zaměstnání" (OrganizationUser.employmentDismissed)
   * - roleCentralniNakup
     - Seznam rolí pro přístup do aplikace Centrální nákup.
     - "Uživatel zřizované organizace"."Role centrálního nákupu zřizované organizace" (OrganizationUser. OrganizationCentralPurchaseRole)
   * - …/item
     - ID role
     - "Role centrálního nákupu zřizované organizace"."kód" (OrganizationCentralPurchaseRole.code)

.. admonition:: Příklad odpovědi CreateOrganizationUserResponse
   :class: info

   .. literalinclude:: _static/xml/CreateOrganizationUserResponse.xml
      :language: xml
      

.. list-table:: Popis atributů ``CreateOrganizationUserResponse``
   :header-rows: 1

   * - Název
     - Popis
     - Atribut z datového modelu
   * - object-id
     - Přihlašovací jméno uživatele zřizované organizace.
     - "Uživatel zřizované organizace"."přihlašovací jméno" (OrganizationUser.loginName)

     
.. _ws:updateorganizationuser:

UpdateOrganizationUser
----------------------

Metoda UpdateOrganizationUser na základě požadavku ``UpdateOrganizationUserRequest`` provede změnu údajů uživatele zřizované organizace pod daným subjektem a v odpovědi ``UpdateOrganizationUserResponse`` se vrací výsledek provedené akce. Metoda používá stejné elementy jako ``CreateOrganizationUserRequest``. Uvádí se jen ty elementy, jejichž hodnoty se mění; atribut ``object-path`` a ``object-id`` jsou povinné a identifikují organizaci a uživatele, jehož údaje se mění.

.. admonition:: Příklad žádosti UpdateOrganizationUserRequest
   :class: info

   .. literalinclude:: _static/xml/UpdateOrganizationUserRequest.xml
      :language: xml

.. admonition:: Příklad odpovědi UpdateOrganizationUserResponse
   :class: info

   .. literalinclude:: _static/xml/UpdateOrganizationUserResponse.xml
      :language: xml
