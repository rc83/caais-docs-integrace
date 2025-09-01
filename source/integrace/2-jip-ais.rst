===============================
Migrace AIS z JIP/KAAS na CAAIS
===============================

*Tato kapitola poskytuje základní přehled migrace z JIP na CAAIS pro garanty AIS z pohledu procesního i technického.*

.. admonition:: Oslovení uživatelů
   :class: note

   Úspěšná migrace závisí především na poskytnutí klíčových informací uživatelům, aby měli zajištěn přístup do systému CAAIS a přidělena odpovídajících oprávnění. Vzhledem k plánované hromadné migraci několika desítek AIS nabízíme metodickou podporu a koordinaci při jejich informování.


**TL;DR:** Technicky je přechod AIS z CAAIS na JIP/KAAS poměrně snadný díky zachování zpětné kompatibility autentizačního protokolu. Současně však CAAIS poskytuje možnosti, jak se při generační obměně AIS zbavit závislosti na zastaralém proprietárním protokolu ve prospěch některého ze současných standardů – OIDC a SAML 2.0.



Strategie přechodu
==================

Autentizační a autorizační informační systémy (AAIS) CAAIS a JIP/KAAS mohou být používány k přihlášení do AIS souběžně a nezávisle. Je tak možné volit ze dvou základních strategií přechodu: **Sunrise & Sunset** a **Big Bang**.


Sunrise & Sunset: Dočasný souběh 
--------------------------------

AIS po přechodnou dobu umožní souběžné přihlašování uživatelů jak pomocí, JIP/KAAS, tak pomocí CAAIS. Přechodná doba trvající 6–9 měsíců současně pokrývá uvedení CAAIS (sunrise period) a vyřazení JIP/KAAS (sunset period). AIS je potřeba upravit, aby umožňoval přihlašování z více systémů, což je ale v případě zachování JIP/KAAS protokolu úprava spíše drobnější.

Obvyklý harmonogram
~~~~~~~~~~~~~~~~~~~

1. Úprava AIS, aby podporoval více autentizačních systémů současně.
#. Integrace vývojového prostředí AIS proti integračnímu (testovacímu) CAAIS.
#. Vytvoření konfigurace AIS v produkčním CAAIS a nastavení infrastruktury (firewall).
#. Nasazení verze AIS s podporou JIP/KAAS a CAAIS do produkce. Počátek sunrise period pro CAAIS a sunset period pro JIP/KAAS.
#. Komunikace s uživateli na počátku sunrise period CAAIS.
#. Komunikace s uživateli před koncem sunset period JIP/KAAS.
#. Ve vhodném okamžiku znepřístupnit či odstranit podporu JIP/KAAS.

Kalendářně odhadujeme trvání kroků 1–4 na dva až tři měsíce, zejména kvůli rychlosti uzavření smlouvy na úpravy AIS a kapacit na straně dodavatele.

Analýza kladů a záporů
~~~~~~~~~~~~~~~~~~~~~~

Hlavní výhodou této strategie je napojení AIS na CAAIS bez nutnosti koordinace s uživateli.

Výhody
......

- nižší riziko selhání
- lepší uživatelská zkušenost
- není nutná těsná koordinace s uživateli


Nevýhody
........

- vyžadována úprava AIS dodavatelem
- z důvody napojení na dva systémy složitější správa a podpora
- zachování JIP/KAAS legacy: absence funkcionalit dostupných jen pro standardní protokoly


Strategie Sunrise & Sunset je vhodná zejména pro větší systémy nebo systémy s velkým počtem uživatelů.


Big bang: Velký třesk
---------------------

Velký třesk představuje scénář, kdy se autentizace a autorizace do AIS náhle (obvykle o víkendu) přepojí z JIP/KAAS na CAAIS. V pátek se tak ještě všichni uživatelé přihlašují pomocí JIP/KAAS, v pondělí už pomocí CAAIS. Pro úspěch je naprosto zásadní komunikace s uživateli a jejich součinnost.

Je možné rozlišit dva dílčí scénáře. V prvním případě zůstává zachována stávající verze AIS, jen se změní konfigurace AIS pro napojení na CAAIS, což předpokládá použití JIP/KAAS (legacy) protokolu. V druhém případě vzniká nová verze AIS, která opouští překonaný JIP/KAAS protokolu ve prospěch některého ze standardních protokolů OIDC a SAML 2.0.

Obvyklý harmonogram
~~~~~~~~~~~~~~~~~~~

1. Integrace neprodukčního prostředí AIS proti integračnímu (testovacímu) CAAIS.
#. Vytvoření konfigurace AIS v produkčním CAAIS – zejména přístupové role.
#. Komunikace s uživateli, aby si zajistili nastavení potřebných oprávnění (přístupových rolí) v CAAIS.
#. Dokončení konfigurace AIS (certifikáty, endpointy) v produkčním CAAIS.
#. Velký třesk. Změna konfigurace AIS; nastavení infrastruktury AIS (firewall)
#. Dočasně zvýšené nároky na L1 podporu AIS a CAAIS.

Kalendářně odhadujeme trvání na jeden až tři měsíce, zejména z důvodu komunikace s uživateli v kroku 3.

Analýza kladů a záporů
~~~~~~~~~~~~~~~~~~~~~~
   
Výhody
......

- rychlé provedení změny
- jednodušší správa a podpora (napojení jen na jeden systém)
- při zachování JIP/KAAS legacy: není nutná úprava AIS, vše je záležitost konfigurace
- při implementaci standardního protokolu:* dostupnost nových funkcionalit


Nevýhody
........

- vysoké riziko výpadku
- potřeba těsné koordinace s uživateli
- riziko nedostatečné součinnosti uživatelů

Strategii Big Bang lze doporučit pro malé systémy s omezeným počtem uživatelů a dále představuje vhodnou volbu při generační obměně AIS. Jeví se též pragmatickým rozhodnutím pro systémy, kde by provedení i drobných úprav stran vývoje bylo náročné.


Technické podrobnosti
=====================

Dostupné protokoly
------------------

CAAIS nabízí nabízí dva standardní protokoly :ref:`OIDC <api_oidc>` a :ref:`SAML 2.0 <api_saml>` a protokol :ref:`JIP/KAAS (legacy) <api_jip>` pro zajištění co největší zpětné kompatibility. U stávajících systémů obvykle představuje optimální volbu setrvání u JIP/KAAS (legacy) a jeho opuštění až v případě generační obměny AIS či požadavku na funkcionalitu, kterou poskytují jen standardní protokoly.

Adresní rozsah
--------------

V případě protokolů OIDC a JIP/KAAS (legacy) je nutné vést v patrnosti, že infrastruktura na straně AIS musí umožňovat komunikaci na IPv4 a IPv6 rozsah CAAIS API, který je jiný než u JIP/KAAS. Při využití protokolu SAML 2.0 se vlastní autentizace děje výhradně zasíláním zpráv přes webový prohlížeč; přístup k CAAIS je pak nutný pouze k získání autokonfiguračního souboru.


Migrace konfigurací
===================

Konfigurace systémů registrovaných v JIP/KAAS byly do CAAIS zmigrovány k 2. červnu 2026. Spolu se samotnou konfigurací se přeneslo i přiřazení přístupových rolí na subjekty. Konfigurace AIS tak není nutné v CAAIS manuálně zakládat.

Získání přístupu do CAAIS
-------------------------

Požádejte svého lokálního administrátora CAAIS o zřízení uživatelského účtu v CAAIS, pokud jej ještě nemáte, a o přidělení role garanta AIS u požadované konfigurace AIS. Lokálního administrátora CAAIS na svém úřadu oslovíte obvykle stejným způsobem jako lokálního administrátora JIP/KAAS.

Úprava konfigurace
------------------

Ke zprovoznění zmigrované konfigurace AIS protokolem JIP/KAAS (legacy) slouží následující check-list:

- ☐ Zkontrolovat údaje.
- ☐ Nastavit povolené domény (CMS, Internet).
- ☐ Upravit URL endpointů pro autentizaci a odhlášení.
- ☐ Přidat autentizační certifikát.
- ☐ Změnit stav AIS na aktivní.

Na straně AIS pak:

- ☐ Umožnit komunikaci na IP rozsah CAAIS API.
- ☐ Upravit URL endpointů pro autentizaci a odhlášení.


.. admonition:: Omezení protokolu JIP/KAAS (legacy)
   :class: warning

   Pro každou konfiguraci jest lze mít povolenu jen jednu doménu. Pokud má být AIS dostupný jak z Internetu, tak (ostrovně) z CMS, je nutné mít dvě konfigurace.

   V daném prostředí CAAIS jest lze použít jeden autentizační certifikát nejvýše pro jednu konfiguraci AIS. Certifikát totiž slouží nejenom k autentizaci AIS, ale i k jednoznačné identifikace konfigurace.


Převod uživatelských účtů
=========================

Migrace uživatelů *není* činnost správce AIS. Uživatelské účty spravuje lokální administrátor dané instituce (úřadu, subjektu). CAAIS poskytuje lokálnímu administrátorovi migrační nástroj pro převod celého uživatelského kmene daného úřadu z JIP. Nelze tak migrovat jen uživatele určitého AIS. Je na zvážení dané instituce, kdy či zda vůbec migraci provede; místo migrace může uživatele v CAAIS dočasně zakládat manuálně nebo automatizovaně ze svého IdM řešení.

Spolu s migrací uživatelů jsou přenášeny i jejich role, pokud je v CAAIS založena odpovídající konfigurace AIS.


Mapování uživatelských účtů v AIS
=================================

CAAIS sám o sobě nepodporuje mapování uživatelských účtů a profilů v JIP a CAAIS.

Pokud AIS zaznamenává údaje o přihlašovaném uživateli výhradně pro účely auditu a neuchovává žádné další informace (jako například uživatelské předvolby), vystačí si s údaji získanými z CAAIS a nepotřebuje provádět žádné mapování uživatelů.

V případě AIS, který uchovává údaje o uživateli a zároveň má umožnit jejich přístup bez ohledu na to, zda se uživatel přihlásil prostřednictvím JIP/KAAS nebo CAAIS, je nutné spárovat jeho identitu v obou systémech. Nejbezpečnějším řešením je, aby se uživatel, již přihlášený přes CAAIS, v rámci otevřeného sezení jednorázově ověřil také přes JIP. Tímto způsobem lze uživatelovy údaje v AIS bezpečně propojit.

Pokud si AIS o uživateli ukládá jen pomocné údaje nedůležité povahy, postačuje pro lepší uživatelský zážitek nabídnout import údajů na základě heuristiky.


.. admonition:: Použití username a BSI
   :class: warning

   Při migraci uživatelských účtů z JIP se sice přenáší username, ale obecně nelze garantovat, že uživatel bude mít stejný username v CAAIS, jako má v JIP.
   
   Obvyklé případy, kdy username neodpovídají:
   
   - Uživatel byl v CAAIS založen dříve pod jiným uživatelským jménem. 
   - Jiný uživatel byl v CAAIS dříve založen po tímto uživatelským jménem.
   
   BSI (UUID) profilu se v CAAIS generuje znovu, při migraci se nepřenáší.


Pro osoby identifikované v AIS AIFO chystáme službu ztotožnění přihlášeného uživatele přes IS ORG.

.. admonition:: Identifikace uživatelského účtu v CAAIS
   :class: warning
   
   Pro persistentní identifikaci uživatelského účtu v CAAIS používejte výhradně BSI. Uživatelské jméno a jméno profilu se může měnit.



Často kladené otázky
====================

*zatím prázdné*

Další zdroje
============

- :ref:`tutorial_jip`
- :ref:`api_jip`

Kontakt a podpora
=================

Pokud máte v úmyslu migrovat svůj AIS z JIP/KAAS do CAAIS, kontaktujte nás prosím přes `Service Desk DIA`_. Pro urychlení komunikace tiket pojmenujte „Migrace AIS {zkratka AIS} do CAAIS“. Následně se domluvíme na on-line schůzce, kde společně vypracujeme plán přechodu po procesní i technické stránce.

.. _Service Desk DIA: https://portal.szrcr.cz/ 
