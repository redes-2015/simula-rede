#!/bin/bash
# Script que executa o simulador de redes com maior facilidade

# Diretório do projeto
DIR=`cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd`

SRCDIR="src"       # Diretório contendo código fonte
DATADIR="data"     # Diretório contendo arquivos de teste
SLIDEDIR="slides"  # Diretório contendo os slides

# Nome do tar.gz e a pasta nele contido a serem entregues no PACA
TARNAME="ep3.tar.gz"
TARDIR="ep3-evandro-leonardo"

# --------------------------------------------------------------------
# Mostra como usar o script

function uso {

    echo -e "\e[1mUSO\e[0m"
    echo -e "\t./`basename $0` <\e[1mArquivo de simulação\e[0m> [\e[1m-h\e[0m] [\e[1m-t\e[0m]\n"

    echo -e "\e[1mDESCRIÇÃO\e[0m"
    echo -e "\tExecuta o simulador de redes usando o arquivo de entrada especificado."
    echo -e "\tSupõe-se que o arquivo esteja no formato correto e que seja dado como"
    echo -e "\to primeiro argumento deste script.\n"

    echo -e "\tLocalização do executável:"
    echo -e "\t'${SRCDIR}/main.py'\n"

    echo -e "\e[1mOPÇÕES ADICIONAIS\e[0m"
    echo -e "\tSepare cada opção com um espaço.\n"

    echo -e "\t\e[1m-h\e[0m\tMostra como usar o script, além de abandoná-lo.\n"

    echo -e "\t\e[1m-t\e[0m\tCria um tar.gz com os arquivos a serem entregues no PACA,"
    echo -e "\t\talém de abandonar o script."

    exit
}

# --------------------------------------------------------------------
# MAIN

# Verifica argumentos adicionais
for arg in "$@"; do
    case $arg in
    -h)
        uso;;
    -t)
        mkdir -p $TARDIR
        cp -rf README.txt executa.sh $SRCDIR $TARDIR
        cp -rf $DATADIR $TARDIR/$SRCDIR
        libreoffice --headless --convert-to pdf --outdir $TARDIR $SLIDEDIR/slides.odp
        mv $TARDIR/README.txt $TARDIR/LEIAME
        find $TARDIR -name __pycache__ | xargs rm -rf
        tar -cvf $TARNAME $TARDIR
        rm -rf $TARDIR
        echo -e "Arquivo \e[1;31m$TARNAME\e[0m criado com sucesso!"
        exit 0;;
    esac
done

# Executa o programa
python3 $SRCDIR/main.py $1
