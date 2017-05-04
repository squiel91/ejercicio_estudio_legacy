#!/bin/bash/

echo 'Actualizando apt-get...'
then sudo apt-get update -y;  

echo 'Instalando Git..'
sudo apt-get install git -y

echo 'Clonando repositiorio..'
git -c user.name='anonimo' -c user.email='anonimo@email.org' clone https://github.com/squiel91/ejercicio_estudio.git

echo 'Installando Pip'
sudo apt-get install -y python3-pip

echo 'Installing librerias..'
pip3 install -r ejercicio_estudio/supereval/requeriments.txt

echo 'Instalando paquete latex..'
sudo apt-get install texlive-latex-extra

echo 'Listo!'
cd ejercicio_estudio/

