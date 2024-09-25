from Rotas import Entradas
import googlemaps
import os
from dotenv import load_dotenv
#função principal para capturar rotas e clima
def main():
    #instanciando o cliente do google maps
    load_dotenv()
    api_key = os.getenv("api_key")
    gmaps=googlemaps.Client(api_key)

    try:
    #Criando uma instância da classe Entradas 
        entrada=Entradas(gmaps) #passando o cliente como parâmentro
        entrada.definir_partida() #chamando a função definir partida
        destino=entrada.definir_destino()#chamando a função definir destino
        entrada.preferencia_rotas() #chamando a função preferencia de rotas

        #Buscando rotas com base nas entradas definidas.
        entrada.buscar_rotas()

    except Exception as e: 
        print(f'Ocorreu um erro: {e}')

if __name__ == "__main__":
    main()

