#!/bin/zsh

endpoint='https://externaleditapi10.caais-test-ext.gov.cz/spravadat/ws/call/DIACZ'
username='local_admin'
password='secret_password'

curl -i \
  -u $username:$password --basic \
  -H 'Content-Type: text/xml' \
  --data-raw '<GetVersionRequest xmlns="http://userportal.novell.com/ws/WS-LA-1.0"/>' \
  $endpoint
