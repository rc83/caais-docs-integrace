====
Úvod
====

.. include:: deprecation-warning.inc.rst

Účelem tohoto dokumentu je popsat technické detaily uživatelské autentizace do agendových informačních systémů (AIS), které jsou registrovány v systému CAAIS.

Uživatel se přihlašuje do systému s využitím CAAIS-IdP (modul interního IdP CAAIS), který zde plní funkci autentizačního informačního systému dle `§ 56a zákona č. 111/2009 Sb., o základních registrech <zr_>`_. Alternativně se může uživatel přihlašovat pomocí NIA (identitu občana), zřízenou `zákonem č. 250/2017 Sb., o elektronické identifikaci <nia_>`_. Pro AIS je zcela transparentní, který IdP byl v CAAIS použit.

.. _zr: https://www.e-sbirka.cz/sb/2009/111#par_56a
.. _nia: https://www.e-sbirka.cz/sb/2017/250

Komunikace a předávání údajů o uživateli probíhá pomocí SOAP protokolu JIP/KAAS legacy, který se využívá pro výměnu autentizačních a autorizačních dat. Protokol vychází z `původního proprietárního protokolu systému JIP/KAAS <jip_>`_ pro zajištění zpětné kompatibility.

.. _jip: https://www.czechpoint.cz/data/formulare/files/popis_WS_KAAS-JIP.zip

Pro autentizaci lze využít dva mechanismy, přičemž pravděpodobně budete chtít využívat autentizaci klasickou.

   - :ref:`api_jip:techspec`
   - :ref:`api_jip:techspec_prima`
