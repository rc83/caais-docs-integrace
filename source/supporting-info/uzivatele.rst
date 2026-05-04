.. _si:users:

======================
Uživatelské účty CAAIS
======================

Při zakládání nového uživatelského účtu v CAAIS lze zvolit username dle výběru uživatele. Ve většině případů je první předgenerovanou hodnotou username ve tvaru **jmeno_prijmeni**, nicméně lze zvolit i vlastní hodnotu. Pokud chce uživatel přenést původní username z JIP/KAAS, je možné si jej zvolit, pokud není již zabráno jiným uživatelem, případně nelze username upravit, pokud již byl uživatel v systému ztotožněn pod jiným uživatelským profilem. Obecně není vhodné vázat uživatele na username, ale na BSI, respektive UUID daného uživatele, tedy unikátní identifikátor.

Při integraci uživatelů v AIS je možné profily z JIP/KAAS a CAAIS vzájemně integrovat následujícími způsoby:

1. Uživatel se do AIS přihlásí pomocí CAAIS a systém ho vyzve aby se přihlásil znovu pomocí JIP/KAAS. Po úspěšném přihlášení se oba profily zintegrují a uživatel bude mít přístup k datům z obou profilů.

2. Uživatel bude mít v AIS vytvořeny dva samostatné profily, jeden pro JIP/KAAS a druhý pro CAAIS. Uživatel se bude muset přihlašovat do AIS pomocí obou profilů, původní agendy dokončí v rámci profilu z JIP/KAAS, nové agendy začne vykonávat v rámci profilu z CAAIS.

3. Na základě heretické úpravy se uživateli po přihlášení přes CAAIS zintegrují uživatelské role, které jsou nezbytné k výkonu dané agendy.