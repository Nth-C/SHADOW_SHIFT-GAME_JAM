#!/bin/sh
python3.12 -m venv .venv

source .venv/bin/activate

pip install -U pip 

pip install -e .

echo "Commande pour activer l'environnement :"
echo "    source .venv/bin/activate"