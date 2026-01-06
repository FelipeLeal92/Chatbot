#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Instalando dependências do Python ---"
pip install -r backend/requirements.txt

echo "--- Construindo o Frontend (Widget) ---"
cd frontend
npm install
npm run build
cd ..

echo "--- Movendo Frontend para o Backend ---"
# Cria a pasta static dentro do app Python e copia o build do React para lá
mkdir -p backend/app/static
cp -r frontend/dist/* backend/app/static/
echo "--- Build concluído com sucesso! ---"