#!/bin/zsh

endpoint='https://cert-externaleditapi11.caais-test-ext.gov.cz/spravadat/ws-edit/1/call/DIACZ'

curl -i \
  --key idm.key --cert idm.crt \
  -H 'Content-Type: text/xml' \
  --data-raw '<GetVersionRequest xmlns="http://userportal.novell.com/ws/WS-LA-1.1"/>' \
  $endpoint
