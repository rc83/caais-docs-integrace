.. _ws:edit-2:

=============================================================
Metody webové služby se specializovanými metodami (WS-EDIT/2)
=============================================================

Specializované metody jsou dostupné pouze ve **verzi 1.1** webových služeb. Podrobně je syntaxe metod popsána ve schématu :download:`XSD editačních služeb 1.1, část 2<_static/xsd/ws-11-2.xsd>`.

.. contents:: Metody WS-EDIT/2
   :local:
   :depth: 2

.. list-table:: Jmenný prostor metod WS-EDIT/2
   :header-rows: 1

   * - Verze
     - XMLNS
     - Endpoint [#endpoint]_
   * - 1.1
     - http\://userportal.novell.com/ws-edit/2/WS-2-1.1
     - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/2/call/exampleId

.. [#endpoint] zde je uveden jen příklad endpointu; v úplnosti :ref:`ws11:endpoints`

Ztotožnění uživatele
====================

.. _ws:identifyagainstrob:

IdentifyAgainstRob
------------------

Metoda IdentifyAgainstRob na základě požadavku ``IdentifyAgainstRobRequest`` provede ztotožnění uživatele přiřazením :abbr:`AIFO (Agendový Identifikátor Fyzické Osoby)`, a to buď nalezením uživatele v CAAIS, pokud již existuje, anebo voláním metody `E278 – robCtiPodleUdaju2`_ základních registrů. V odpovědi ``IdentifyByRobResponse`` se vrací výsledek provedené akce.

Uživatelský profil musí být ve stavu „Před ztotožněním“, případně „Aktivní“. Po úspěšném ztotožnění jsou zneplatněny odkazy na samoztotožnění, které byly uživateli zaslány e-mailem při :ref:`založení profilu <ws:createuser>`.


.. dropdown:: CAAIS Internals
   :color: muted
   :icon: gear
   
   V systému CAAIS se provádí následující kroky:
   - Pokus o nalezení Profilu podle atributu WS „username“ (odpovídá atributu CAAIS "Profil"."uživatelské jméno" (Profile.loginName)).
  
     - Pokud není Profil nalezen, vrací se chyba.
     - Pokud není odpovídající FO pro daný Profil ve stavech „Před ztotožněním“/„Aktivní“ vrací se chyba.
     - Pokud má odpovídající FO pro daný Profil atribut „Osoba evidována v ROB“ (personInRob) = "Ne" (jedná se o neztotožnitelnou osobu) a zároveň je FO ve stavu "Aktivní", vrací se chyba.
     - Pokud je Profil nalezen a FO má atribut "Osoba evidována v ROB" (personInRob) = "Ano", vrací se OK (FO již byla ztotožněna).

   - Pokud je FO pro profil ve stavu "Před ztotožněním" provedou se tyto kroky:

     - Volá se ROB metoda `E278 – robCtiPodleUdaju2`_ s parametry

       - buď jméno ("Fyzická osoba"."jméno" (PhysicalPerson.firstName)) + příjmení ("Fyzická osoba"."příjmení" (PhysicalPerson.lastName)) + datum narození z atributu WS "dateOfBirth" (+ volitelně místo narození z atributu WS "placeOfBirth"),
       - anebo druh a číslo dokladu z atributu "identificationCard" WS.

     - Pokud není FO v ROB nalezena vrací se chyba.
     - Pokud je FO v ROB nalezena, provedou se tyto kroky:
    
       - Pokus o nalezení vráceného AIFO v mapování federačního hubu CAAIS (tabulka IdentityMapping)
       - Pokud není AIFO nalezeno provedou se tyto kroky:
    
         - Nastaví se atribut FO "Osoba evidována v ROB" (personInRob) = "Ano"
         - Stav FO se nastaví na "Aktivní"
         - Stav Profilu se ponechá ve stavu dle požadavku metody CreaterUser ("Aktivní"/"Neaktivní")
         - Doplní se mapování AIFO ve federačním hubu (tabulka IdentityMapping)
         - Volá se ROB metoda `E45 – orgPrihlasAifo`_ pro zaregistrování daného AIFO k notifikaci změn v ROB pro systém CAAIS.
         - Do systému CAAIS-IdP volá založení nové identity s údaji FO (certifikáty uloženy v pomocné technické tabulce "Certifikát pro samoztotožnění")
         - Z pomocné technické tabulky "Certifikát pro samoztotožnění" se smažou dočasně uložené certifikáty dané FO
         - Zneplatní se odkaz na stránku pro samoztotožnění, předávaný emailem uživateli, aby se uživatel nepokoušel znovu ztotožnit
       - Pokud je AIFO nalezeno, znamená to, že již v CAAIS existuje ztotožněná FO pro zadané údaje a že se má nově založený profil navázat na tuto FO a provedou se tyto kroky:
    
         - Profil se naváže na existující FO s nalezeným AIFO
         - Stav FO se nastaví na "Aktivní", pokud takový stav již nemá nastaven (byla v minulosti deaktivována)
         - Stav Profilu se ponechá ve stavu dle požadavku metody CreaterUser ("Aktivní"/"Neaktivní")
         - Původně založená FO pro daný profil ve stavu "Před ztotožněním" se smaže


.. admonition:: Příklad žádosti IdentifyAgainstRobRequest
   :class: info
   
   .. literalinclude:: _static/xml/IdentifyAgainstRobRequest.xml
      :language: xml

    
.. list-table:: Popis atributů ``IdentifyAgainstRobRequest``
    :header-rows: 1

    * - Název
      - Popis
    * - username
      - Uživatelské jméno pro ztotožnění.
    * - dateOfBirth
      - Datum narození osoby.
    * - placeOfBirth
      - Místo narození osoby.
        Pokud je osoba narozena v ČR, vyplňuje se kód obce.
        Pokud je osoba narozena mimo ČR, vyplňuje se název obce + atribut countryCode (viz níže).
    * - countryCode
      - Pokud je místo narození mimo ČR, zadává se i stát narození jako číselný kód ISO 3166-1.
    * - identificationCard
      - Číslo dokladu totožnosti.
    * - …/type
      - Druh dokladu totožnosti jako :ref:`ws:ciselnik:doklad`

Pro volání do ROB je nutné zadat jen atribut ``identificationCard``, anebo ``dateOfBirth``; atribut ``placeOfBirth`` je nutné vyplnit pouze v případě, že kombinace jména, příjmení a data narození nedostačuje k jednoznačné identifikaci osoby v ROB (bylo nalezeno více záznamů). Podrobněji dokumentace podkladové služby `E278 – robCtiPodleUdaju2`_ základní registrů, povolené kombinace údajů II a IV.

.. _ws:ciselnik:doklad:

.. list-table:: Číselník typu dokladu totožnosti
   :header-rows: 1

   * - Kód
     - Typ dokladu totožnosti
   * - ID
     - Občanský průkaz
   * - P
     - Cestovní pas
   * - IR
     - Povolení k pobytu
   * - VZ
     - Vízový štítek
   * - PS
     - Pobytový štítek
   * - OP
     - Občanský průkaz bez MRZ
   * - CA
     - Cestovní průkaz
   * - IX
     - Knížečka (označení CIS: PB, PE, PO, PP, PR)
   * - IE
     - Tiskopis (označení CIS: PM, OR)


.. _E278 – robCtiPodleUdaju2: https://www.szrcr.cz/images/dokumenty/v%C3%BDvoj%C3%A1%C5%99i/detailn%C3%AD_popisy_eGon_slu%C5%BEeb/SZR_popis_eGON_sluz%CC%8Ceb_E278_robCtiPodleUdaju2.pdf
.. _E45 – orgPrihlasAifo: https://szrcr.cz/images/dokumenty/v%C3%BDvoj%C3%A1%C5%99i/detailn%C3%AD_popisy_eGon_slu%C5%BEeb/SZR_popis_eGON_slu%C3%9Feb_E45_orgPrihlasAIFO_v6.pdf

.. admonition:: Příklad odpovědi IdentifyAgainstRobResponse
   :class: info
   
   .. literalinclude:: _static/xml/IdentifyAgainstRobResponse.xml
      :language: xml


      
Spravované subjekty
===================

.. _ws:getmanageablesubjects:

GetManageableSubjects
---------------------

Metoda GetManageableSubjects na základě požadavku ``GetManageableSubjectsRequest`` vrací v odpovědí ``GetManageableSubjectsResponse`` seznam subjektů (jejich zkratek), ke kterým má daný subjekt povolen přístup díky přenesené působnosti lokálního administrátora (čtení i zápis) nebo přenesené působnosti čtení dat subjektu (jen čtení). V odpovědi se krom podřízených subjektů vrací také daný subjekt, pro který se metoda volá.

.. admonition:: Příklad žádosti GetManageableSubjectsRequest
   :class: info
   
   .. literalinclude:: _static/xml/GetManageableSubjectsRequest.xml
      :language: xml
      
.. admonition:: Příklad odpovědi GetManageableSubjectsResponse
   :class: info
   
   .. literalinclude:: _static/xml/GetManageableSubjectsResponse.xml
      :language: xml
      
.. list-table:: Popis atributů ``GetManageableSubjectsResponse``
    :header-rows: 1

    * - Název
      - Popis
      - Atribut z datového modelu
    * - subjects
      - Seznamam subjektů.
      - Vrací volající subjekt a subjekty uvedené v entitě "Působnost" (Authority) v atributu "zdrojový subjekt", pro něž je volající subjekt v atributu "cílový subjekt". Jedná se o všechny působnosti, které byly předány danému subjektu od jiných subjektů.
    * - item
      - Jeden subjekt v seznamu.
      -
    * - …/name
      - Zkratka subjektu
      - "Subjekt"."zkratka" (Subject.shortcut)
    * - …/LaDelegationRights
      - Vrací se informace o nastavení přenesené působnosti lokálního administrátora (právo ke čtení i zápisu).
        Hodnota „inactive“ znamená, že cílový (tzn. metodu volající) subjekt ještě nepřijal přenesenou působnost od zdrojového subjektu.
        Hodnota „active“ znamená, že působnost byla přijata.
      - pokud "Působnost"."Typ působnosti"."název" (Authority.AuthorityType.name) = "Lokální administrátor)"

        = active, pokud "Působnost"."působnost potvrzena" (Authority.confirmed) = "ano"

        = inactive, pokud "Působnost"."působnost potvrzena" (Authority.confirmed) = "ne"
    * - …/ReaderDelegationRights
      - Vrací se informace o nastavení přenesené působnosti čtení dat subjektu (právo pouze ke čtení).
        Hodnoty „inactive“ a „active“ mají stejný význam jako v atributu LaDelegationRights.
      - pokud "Působnost"."Typ působnosti"."název" (Authority.AuthorityType.name) = "Čtení dat jiného subjektu"

        = active, pokud "Působnost"."působnost potvrzena" (Authority.confirmed) = "ano"

        = inactive, pokud "Působnost"."působnost potvrzena" (Authority.confirmed) = "ne"

Subjekt, pro který se metoda volá (cílový, resp. nadřízený) má nastaveny oba atributy „LaDelegationRights“ a „ReaderDelegationRights“ na hodnotu „active“.


Historie změn údajů
===================

.. _ws:historydata:

HistoryData
-----------

Metoda HistoryData na základě požadavku ``HistoryDataRequest`` vrací v odpovědi ``HistoryDataResponse`` seznam změněných údajů v CAAIS za definované časové období.

.. admonition:: Není implementováno
   :class: error
   
   Metoda se právě doimplementovává.



Dovolené hodnoty číselníků
==========================

.. _ws:getlistofvalues:

GetListOfValues
---------------

Metoda GetListOfValues na základě požadavku ``GetListOfValuesRequest`` vrací v odpovědí ``GetListOfValuesResponse`` číselníky hodnot používané v editačních webových službách CAAIS. Na vstupu se definuje název číselníku, jehož hodnoty se mají vrátit.

.. admonition:: Příklad žádosti GetListOfValuesRequest
   :class: info
   
   .. literalinclude:: _static/xml/GetListOfValuesRequest.xml
      :language: xml


.. list-table:: Popis atributů ``GetListOfValuesRequest``
    :header-rows: 1

    * - Název
      - Popis
    * - listName
      - Název (kód) číselníku dle :ref:`ws:ciselnik:ciselniky`.


      
.. _ws:ciselnik:ciselniky:
      

.. list-table:: Seznam číselníků
    :header-rows: 1

    * - Název
      - Popis
    * - ais_role
      - Číselník přístupových rolí do všech AIS v systému, které definují garanti daných AIS. Hodnoty se používají v atributu „aisRole“ v metodách :ref:`ws:getsubject`, :ref:`ws:getuser`, :ref:`ws:createuser` a :ref:`ws:updateuser`.
        Vrací se všechny aktivní "Přístupové role".
    * - ciselnik_statu
      - Číselník států, jehož hodnoty se předávají v atributu „countryCode“ v metodě :ref:`ws:identifyagainstrob`.
        Vrací se seznam států z tabulky "Stát".
    * - szr_role
      - Číselník agendových činnostních rolí pro přístup do základních registrů. Hodnoty se používají v atributu „cinnostniRole“ v metodách :ref:`ws:getsubject`, :ref:`ws:getuser`, :ref:`ws:createuser` a :ref:`ws:updateuser`. Vrací se jen aktivní činnostní role v aktivních agendách.

      
.. admonition:: Příklad žádosti GetListOfValuesResponse
   :class: info
   
   .. literalinclude:: _static/xml/GetListOfValuesResponse.xml
      :language: xml

.. list-table:: Popis atributů ``GetListOfValuesResponse``
    :header-rows: 1

    * - Název
      - Popis
    * - list
      - Element se seznamem hodnot požadovaného číselníku.
    * - …/name
      - Název číselníku.
    * - …/type
      - Datový typ pro hodnoty v číselníku (binary, string, structured).
    * - item
      - Jedna položka číselníku. Binární hodnoty jsou zakódovány v Base64 kódování.
        
        - Pro číselník typu "ais_role" se vyplňuje ve formátu "<název_přistupové_role> (<název_AIS>) @ <název_subjektu_který_je_garantem_AIS>".
        - Pro číselník typu "ciselnik_statu" se vyplňuje hodnota atributu "Stát"."plný název".
        - Pro číselník typu "szr_role" se vyplňuje název činnostní role.
    * - …/key
      - Interní ID položky v číselníku.
        
        - Pro číselník typu "ais_role" se vyplňuje ve formátu <zkratka_ais>.<zkratka_přístupové_role>.
        - Pro číselník typu "ciselnik_statu" se vyplňuje hodnota atributu "Stát"."kód".
        - Pro číselník typu "szr_role" se vyplňuje ve formátu "<kód_agendy>,<kód_činnostní_role>".
