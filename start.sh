#!/bin/bash

echo "Unzipping folders..."
unzip -o templates.zip -d templates
unzip -o static.zip -d static

echo "Starting app..."
gunicorn app:app
