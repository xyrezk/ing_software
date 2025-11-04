from database import init_db


def main():
    init_db()
    opc=0
    while opc!=9:
        opc=int(input("ingrese que opcion desea "))
        if opc==1:
            print("jeje") 
         
         
        elif opc==9:
            print("chao")
            break
         




main()


