#!/bin/sh

echo " --> Démarrage ..."

sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8501
screen -S pimpon -dm streamlit run chat.py
