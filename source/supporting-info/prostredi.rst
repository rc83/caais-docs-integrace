.. _si:env:

======================
Běhová prostředí CAAIS
======================

CAAIS nabízí tři veřejná prostředí CAAIS. Každé je dostupné jak na rozhraní CMS (cms2.cz), tak Internetu (gov.cz).

URL prostředí mají podobu *https://caais[-zkratka prostředí].<rozhraní>/*, například 

- https://caais.cms2.cz/ či
- https://caais-test-ext.gov.cz/.

.. list-table:: Běhová prostředí CAAIS
   :header-rows: 1
   :name: caais_env
   :widths: 11 10 50 20

   * - Prostředí
     - Zkratka
     - Účel
     - Garantovaná dostupnost   
   * - `Produkční <prod_>`_
     - —
     - produkční prostředí
     - SLA 99,9 %
   * - `Školicí <edu_>`_
     - edu
     - pískoviště zejména pro lokální administrátory; obnovováno týdně na základě produkční databáze
     - pracovní dni 6.00–18.00
   * - `Integrační <int_>`_
     - test-ext
     - integrační testování připojovaných AIS; omezený dataset a napojení na externí systémy
     - 6.00–22.00



.. _si:env:prod:

Produkční prostředí
-------------------

*zatím prázdné*


.. _si:env:edu:

Školicí prostředí (edu)
-----------------------

`Školicí prostředí <edu_>`_ je určeno zejména lokálním administrátorům k praktickému seznámená s CAAIS a co nejvíce se blíží produkčnímu prostředí.

Databáze školicího prostředí je obnovována v pondělí časně ráno na základě snímku produkční databáze, tudíž jakékoli změny provedené na školicím prostředí jsou pouze dočasné povahy.

.. admonition:: Nastavení hesla
   :class: warning
   
   Z bezpečnostních důvodů jsou při obnově databáze odstraněna uživatelská hesla (resp. příslušný odvozený klíč), proto si uživatel musí před prvním přihlášením v novém týdnu heslo v CAAIS-IdP znovu nastavit, jako by jej zapomněl.


Přihlašování je možné jen prostřednictvím CAAIS-IdP, nikoli NIA (identitou občana).


.. _si:env:int:

Integrační prostředí (test-ext)
-------------------------------

`Integrační prostředí <int_>`_ slouží k integračnímu testování AIS proti CAAIS. To obnáší ověření úspěšného navázání spojení, správného volání API a shody obdržených údajů s očekávanými.

Integrační prostředí nebylo zamýšleno k extenzivnímu testování samotného AIS. Tomu odpovídá i velice omezená množina údajů dostupná v tomto prostředí. Týká se to zejména institucí (subjektů), činnostních rolí a počtu uživatelů.

Integrační prostředí nesdílí s produkčním prostředím žádné údaje, tedy ani uživatelské účty. Uživatelské účty jsou obvykle vytvářeny jako fiktivní a sdíleny napříč integračním týmem daného AIS. Přihlašování je možné jen prostřednictvím CAAIS-IdP.

.. _prod: https://caais.gov.cz/
.. _edu: https://caais-edu.gov.cz/
.. _int: https://caais-test-ext.gov.cz/
