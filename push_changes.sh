#!/bin/bash

# Cambia al directorio del proyecto
cd /Users/alexandersandoval/Documents/GitHub/Docker_Airflow2

# Verifica el estado del repositorio
git status

# Añade todos los cambios al área de preparación
git add .

# Confirma los cambios con un mensaje
git commit -m "Actualización automática"

# Sube los cambios al repositorio remoto
git push origin main

# Ejecuta en la terminal ./push_changes.sh
