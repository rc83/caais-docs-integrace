.. _ws:errors:

==============
Chybové zprávy
==============

Pokud při zpracování požadavku dojde k chybě, vrací editační webové služby chybovou zprávu jako XML ve standardizovaném formátu. Jmenný prostor zprávy odvisí od volaného endpointu dle tabulky :ref:`ws:error:ns`. Seznam kódů a textů chybových zpráv je uveden v tabulce :ref:`ws:error:code`. Text zprávy může být doplněn o další informace upřesňující příčinu chyby.

- :download:`XSD editačních služeb 1.0<_static/xsd/ws-10.xsd>`,
- :download:`XSD editačních služeb 1.1, část 1<_static/xsd/ws-11-1.xsd>`,
- :download:`XSD editačních služeb 1.1, část 2<_static/xsd/ws-11-2.xsd>`,
- :download:`XSD editačních služeb 1.1, část 3<_static/xsd/ws-11-3.xsd>`.

.. _ws:error:ns:

.. list-table:: Jmenné prostory chybových odpovědí
   :header-rows: 1

   * - Endpoint
     - XMLNS
   * - https://externaleditapi10.caais.gov.cz/spravadat/ws/call/exampleId
     - http\://userportal.novell.com/ws/WS-LA-1.0
   * - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/1/call/exampleId
     - http\://userportal.novell.com/ws/WS-LA-1.1
   * - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/2/call/exampleId
     - http\://userportal.novell.com/ws-edit/2/WS-2-1.1
   * - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/3/call/exampleId
     - http\://userportal.novell.com/ws/WS-READ-1.1

     
.. admonition:: Příklad chyby v odpovědi
   :class: info

   .. code:: xml

      <ErrorResponse xmlns="http://userportal.novell.com/ws/WS-LA-1.1">
          <Code>CAPP-0003</Code>
          <Message>Funkce nebyla implementována.</Message>
      </ErrorResponse>


.. admonition:: HTTP stavový kód odpovědi není definován
   :class: warning
   
   Stavový kód odpovědi na úrovni HTTP protokolu není definován. Může být i HTTP 200 OK.

   
.. _ws:error:code:

.. list-table:: Číselník chybových kódů
   :header-rows: 1

   * - Kód chyby
     - Popis chyby
   * - CAPP-0001
     - Došlo k chybě při generování WSDL.
   * - CAPP-0002
     - Došlo k chybě při zpracování requestu.
   * - CAPP-0003
     - Funkce nebyla implementována.
   * - CAPP-0000
     - Jiná chyba aplikace.
   * - CCFG-0001
     - Uživatel má přiřazeno více rolí.
   * - CCFG-0002
     - Uživatel nemá přiřazenu žádnou roli. Jedná se o účet běžného uživatele.
   * - CLDP-číslo
     - Chyba při komunikaci s CAAIS. Uváděné číslo odpovídá chybovému kódu, který vrací CAAIS.
   * - CLDP-0000
     - Jiná chyba při komunikaci s CAAIS.
   * - CSAV-0001
     - Uživatel nemá právo přistupovat k danému objektu.
   * - CSAV-0002
     - Uživatel nemá právo přistupovat k danému atributu.
   * - CURL-001
     - Neplatné volání webové služby.
   * - CURL-002
     - URL pro volání webové služby není kompletní. Chybí část URL se zkratkou subjektu.
   * - CURL-003
     - Bylo voláno URL s nepřístupným subjektem – subjekt buď neexistuje, nebo k němu nemá daný uživatel povolen přístup.
   * - CVAL-0001
     - Není vyplněna hodnota povinného atributu.
   * - CVAL-0002
     - Hodnota atributu neodpovídá platnému vzoru.
   * - CVAL-0003
     - Hodnota atributu je kratší než minimální vyžadovaná délka.
   * - CVAL-0004
     - Hodnota atributu je delší než maximální vyžadovaná délka.
   * - CVAL-0005
     - Hodnota atributu s binárními daty je větší než maximální povolená velikost.
   * - CVAL-0006
     - Uvedená hodnota atributu není možná. Je potřeba vybrat hodnotu ze seznamu.
   * - CVAL-0010
     - Požadavek neodpovídá schématu deskriptoru.
   * - CVAL-0101
     - Není vyplněna hodnota zkratky datového objektu (subjekt, uživatel, úřadovna, atd.).
   * - CVAL-0102
     - Zkratka objektu obsahuje nepovolené znaky. Povoleny jsou pouze znaky: a-z A-Z . _
   * - CVAL-0110
     - Uvedené uživatelské jméno je již použito. Každé uživatelské jméno v CAAIS musí být unikátní.
   * - CVAL-0111
     - Zadaná hesla se neshodují.
   * - SREN-3050
     - Adresa nebyla nalezena.
   * - SREN-3051
     - Bylo nalezeno více adres odpovídajících zadaným parametrům.
   * - SREN-3052
     - Došlo k chybě při pokusu o ověření adresy vůči UIR.
   * - SREN-3060
     - Osoba krizového řízení s daným jménem nebyla nalezena.
   * - SREN-3061
     - Bylo nalezeno více osob krizového řízení pro zadané jméno.
   * - SREN-3070
     - Nelze zpracovat zaslaný certifikát.
   * - SREN-3072
     - Přístupovou roli do AIS nebylo možné uživateli přiřadit, protože není přiřazena subjektu, do nějž uživatel patří.
   * - SREN-3080
     - Nelze ověřit platnost hodnoty; nelze najít hodnotu nadřazeného subjektu.
   * - SREN-3081
     - Nelze přiřadit hodnotu, kterou nemá přiřazenu nadřazený subjekt.
   * - SREN-3091
     - Nebyla nalezena nebo zadána agenda.
   * - SREN-3092
     - Agendovou činnostní roli nebylo možné uživateli přiřadit, protože není přiřazena subjektu, do nějž uživatel patří.
   * - SVAL-3001
     - Heslo musí obsahovat číslici.
   * - SVAL-3101
     - Uživatel nemůže mít současně přístup do ISUI pro obce i stavební úřady.
   * - SVAL-3111
     - Název aplikace AIS musí být unikátní.
   * - SVAL-3112
     - Subjekt nemůže přenášet svoji působnost, pokud je na něj přenesena působnost z jiného subjektu.
   * - SVAL-3121
     - Zkratka subjektu nebyla nalezena.
