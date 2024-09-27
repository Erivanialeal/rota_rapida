from Rotas import Entradas
import googlemaps
import os #importando o módulo 'os' para acessar variáveis de ambiente
from dotenv import load_dotenv #Importa a função load_dotenv da biblioteca dotenv para carregar variáveis de ambiente
#função principal do programa
def main():
    #carrega as variáveis de ambiente dos arquivos .env 
    load_dotenv()
    #obtem os valores da chave da API
    api_key = os.getenv("api_key")
    #Cria um cliente Google Maps usando a chave da API obtida
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

