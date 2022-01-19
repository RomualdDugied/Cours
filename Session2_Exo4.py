#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

def hashage(serial):
    print(f"Hashage du numero {serial}")
    return "A2312EF76C065EA7C7D"

def main():
    # info concernant la connexion à la base de donnée
    dbaddress = "172.82.83.255"
    dbname = "tracability_db"
    dblogin = "user0345"
    dbpassword = "EY374HSOIE/!" 
    # demande à l'opérateur le nom du projet à charger
    proj = input("\x1b[37;1mSaisissez le nom du projet: \x1b[37;0m")       
    # chargement de tous les fichiers du projet
    print("************************************")
    print(f"-- Chargement du projet {proj} --")
    fichier1 = "bootloader.hex"
    print(f">>  {fichier1}...............done")
    fichier2 = "SD.hex"
    print(f">>  {fichier2}...............done")
    fichier3 = "bootstrap.hex"
    print(f">>  {fichier3}...............done")
    fichier4 = "applicatif.hex"
    print(f">>  {fichier4}...............done")  
    print("************************************") 
    # on tourne en boucle
    while True:
        serial = input("\x1b[37;1mMerci de saisir le numéro de série: \x1b[37;0m")
        if serial.isdigit() and (100000<=int(serial)<999999):
            # recherche doublon en base de donnée
            print(f"\x1b[33;1m[Ouverture de la base: {dbaddress} {dbname} {dblogin} {dbpassword}]\x1b[32;0m")
            print(f"\x1b[33;1m[Recherche dans la base de donnée du NS {serial}]\x1b[32;0m")
            # les numéros présents:
            if serial in ["100001", "100002", "100003", "100004"] :
                nombre_resultat_trouve = 1
            else:
                nombre_resultat_trouve = 0
            print("\x1b[33;1m[Fermeture de la base de donnée]\x1b[32;0m") 
            
            if nombre_resultat_trouve == 0:   
                # calcul du code de hashage                
                hashfield = hashage(serial)
                # ---- préparation du projet ----
                # encodage du fichier boot
                print(f"Encodage {fichier1} avec code de Hashage {hashfield}")
                # merge des fichiers
                print(f">> launch command : mergehex -m {fichier1} {fichier2} merge1")
                print(f">> launch command : mergehex -m {fichier3} {fichier4} merge2")
                print(">> launch command : mergehex -m merge1 merge2 mergefinal")
                # programmation de la cible et reset --> retour de True si OK
                print(">> launch_command : nrfjprog --family NRF52 --program mergefinal --chiperase --verify --log")
                print(">> launch_command : nrfjprog --reset")
                prog_res = True
                
                # vérification résultat de la prog
                if prog_res :
                    # informe l'opérateur du résultat
                    print(f"\x1b[32;1mProgrammation terminée (NS{serial})\x1b[32;0m")   
                else:
                    # informe l'opérateur du résultat
                    print(f"\x1b[31;1mProgrammation impossible (NS{serial})\x1b[32;0m")  
                     
                # enregistrement en base de donnée
                print(f"\x1b[33;1m[Ouverture de la base: {dbaddress} {dbname} {dblogin} {dbpassword}]\x1b[32;0m")
                print(f"\x1b[33;1m[Ecriture dans la base de donnée {serial} = {prog_res}]\x1b[32;0m")
                print("\x1b[33;1m[Fermeture de la base de donnée]\x1b[32;0m")   
            else:
                # erreur numéro de série en doublon
                print(f"\x1b[31;1mCe numéro de série a déjà été utilisé!!!!\x1b[37;0m")    
        else:
            # erreur numéro de série invalide
            print(f"\x1b[31;1mLa saisie n'est pas une numéro de série valide!\x1b[37;0m")


if __name__ == "__main__":
    main()