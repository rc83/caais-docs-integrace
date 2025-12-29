.. _ws:utils:

===========================================
Nástroje využívající editační webové služby
===========================================

Pro naši vnitřní potřebu implementujeme v Pythonu nástroje, které volají editačních webových služby CAAIS. Vedle přímého použití hotových utilit jest lze využít modul ``caaisws.py`` pro vytváření vlastních skriptů. V neposlední řadě může nahlédnutí do zdrojového kódu skriptů sloužit jako rozšíření této dokumentace.


Nástroje jsou dostupné na :octicon:`logo-github` https://github.com/rc83/caais-utils. Pull-requests vítány.

.. list-table:: Nástroje
   :header-rows: 1

   * - nástroj
     - použití
   * - ``export_users``
     - exportuje seznam uživatelů z CAAIS (či JIP/KAAS) do CSV souboru
   * - ``import_users``
     - importuje uživatele z CSV souboru do CAAIS;
       vhodné pro hromadné založení většího počtu uživatelů


.. admonition:: Nástroje ve vývoji
   :class: warning

   Nástroje jsou ve vývoji a nedoporučujeme je používat proti produkčním prostředím. Za následky takového použití neneseme žádnou odpovědnost.
