.. _ws:nonimplemented:

=======================
Neimplementované metody
=======================

Není implementována webová služba JIP/KAAS WS-EDIT/5 s metodou GetUserListRole sloužící specifickému účelu pro využití AIS.

Nejsou implementovány metody JIP/KAAS webové služby WS-EDIT/1 pro práci s úřadovnami a se složkami krizového řízení, neboť datový model CAAIS tyto entity neobsahuje.

- Metody pro práci s úřadovnami (WS-EDIT/1)
  
  - GetOfficeList
  - GetOffice
  - CreateOffice
  - UpdateOffice
  - DeleteOffice
  - SearchOffice

- Metody pro práci se složkami krizového řízení (WS-EDIT/1)

  - GetCrisisMgmtList
  - GetCrisisMgmt
  - CreateCrisisMgmt
  - UpdateCrisisMgmt
  - DeleteCrisisMgmt
  - SearchCrisisMgmt
  
Rovněž nejsou implementovány metody, jejichž deklarace se sice vyskytuje v XSD, ale JIP/KAAS je nedokumentuje.

- Nedokumentované metody vyhledávání (WS-EDIT/1)

  - SearchSubject
  - SearchUser
  - SearchDatabox
  - SearchOrganization
  - SearchOrganizationUser

- Ostatní nedokumentované metody (WS-EDIT/2)

  - IsAlive
