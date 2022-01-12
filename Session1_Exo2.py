#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

import datetime

#objectif du code ci dessous:
#prendre ce dataset contenant des infos sur des salariés 
#les retourner dans la console sous la forme:
# Nom: Savary
# Prenom: Richard
# Age: 44 ans
# Status Cadre
# Ancienneté: 21 ans
# ######################

# dataset
# Nom ; Prenom; Status (NonCadre/Cadre); Date Naissance; Date entrée dans l'entreprise
dataset = [
    "Durand;Christine;0;21/06/1973;18/01/1995",
    "Dupont;Emmanuel;1;04/12/1982;02/01/1999",
    "Gallas;Gaston;1;21/06/1975;01/04/1995",
    "Martin;Marie;1;15/09/1972;04/08/1992",
    "Hulot;Sylvie;0;10/02/1977;01/09/1994",
    "Hernandez;Alfonso;0;27/10/1978;02/06/1997",
    "Savary;Richard;1;18/04/1977;02/01/2000"
]


def display_all() -> None:
    l_o_a = []

    for enr in dataset:
        list_info = enr.split(';')
        l_o_a.append(list_info)

    for emp in l_o_a:
        print(f"Nom: {emp[0]}")
        print(f"Prenom: {emp[1]}")
        print(
            f"Age: {int((datetime.datetime.now()-datetime.datetime.strptime(emp[3],'%d/%m/%Y')).days//365.25)} ans")
        if emp[2] == 0:
            print("Status Employé")
        else:
            print("Status Cadre")
        print(
            f"Ancienneté: {int((datetime.datetime.now()-datetime.datetime.strptime(emp[4],'%d/%m/%Y')).days//365.25)} ans")
        print("######################\n\n")


if __name__ == "__main__":
    display_all()
