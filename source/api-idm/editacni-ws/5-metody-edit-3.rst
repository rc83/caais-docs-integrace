.. _ws:edit-3:

=========================================================
Metody webové služba pro čtení údajů subjektu (WS-EDIT/3)
=========================================================

Ve **verzi 1.1** webových služeb je dostupný samostatný endpoint, na kterém lze volat výhradně read-only metody pro správu dat. Podrobně je syntaxe metod popsána ve schématu :download:`XSD editačních služeb 1.1, část 3<_static/xsd/ws-11-3.xsd>`.

.. list-table:: Jmenný prostor metod WS-EDIT/3
   :header-rows: 1

   * - Verze
     - XMLNS
     - Endpoint [#endpoint]_
   * - 1.1
     - http\://userportal.novell.com/ws/WS-READ-1.1
     - https://cert-externaleditapi11.caais.gov.cz/spravadat/ws-edit/3/call/exampleId
     
.. [#endpoint] zde je uveden jen příklad endpointu; v úplnosti :ref:`ws11:endpoints`


Implementovány jsou následující metody:

- :ref:`GetVersion<ws:getversion>`
- :ref:`GetSubject<ws:getsubject>`
- :ref:`GetDataboxList<ws:getdataboxlist>`
- :ref:`GetUserList<ws:getuserlist>`
- :ref:`GetUser<ws:getuser>`
- :ref:`GetOrganizationList<ws:getorganizationlist>`
- :ref:`GetOrganization<ws:getorganization>`
- :ref:`GetOrganizationUserList<ws:getorganizationuserlist>`
- :ref:`GetOrganizationUser<ws:getorganizationuser>`

Metody se až na odlišný jmenný prostor neliší od :ref:`stejnojmenných metod pro správu dat<ws:edit-1>`.


.. admonition:: Odlišný jmenný prostor
   :class: warning
   
   Pokud chcete volat metody pro správu uživatelů na tomto endpointu, je nezbytné změnit jmenný prostor XML zpráv na: http://userportal.novell.com/ws/WS-READ-1.1.
