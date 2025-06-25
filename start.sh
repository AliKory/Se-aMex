#!/bin/bash

# Ejecutar el servidor Flask usando Gunicorn
exec gunicorn -b 0.0.0.0:10000 app:app
