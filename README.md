Simple python proxy to add https capability to your local web server.

It is designed for development purpose: you can use it to check that your
web application runs well when accessed through https.

Scenario:
* you have a web server (e.g. a python application) listening on port localhost:8080
* start `./https-proxy.py`. It will listen on port 8443, manage SSL and forward connections
  to port 8080.
* type https://localhost:8443 in your browser. After you authorize the self-signed certificate,
  the web application should be displayed.

You can change ports 8080 and 8443 by editing file `conf.py`.
