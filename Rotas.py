
from datetime import datetime,timedelta
class Entradas:
    #métado construtor da classe.
    def __init__(self,googlemaps_cliente):
        self.partida = None
        self.destino = None
        self.rotas = []
        self.googlemaps_cliente= googlemaps_cliente


    def definir_partida(self):
        #pedir ao usúario o local de partida,e verificar se a entrada não está vazia

        while True: #estrutura de repetição while,execulta o codigo até a condicão for verdadeira
            partida= input("Local de partida:").strip()#métado usado para remover espços em branco
            if partida:
                self.partida = partida 
                break
            else:
                print("Local de partida não pode está vazio.Tente Novamente.")


    def definir_destino(self):
        while True:
            destino= input("Local do destino:").strip()
            if destino:
                self.destino= destino
                break
            else:
                print("Local de destino não pode está vazio.Tente Novamente.")

    def preferencia_rotas(self):
        opcoes={
            '1': ('tolls','Evitar Pedágio' ),#Evitando pedágios
            '2': ('ferries','Evitar estradas não pavimentadas'), #Evitando estradas não pavimentadas.
            '3': ('traffic','Evitar trânsito'), #Evitando tránsito
            '4': ('shortest','Rota mais curta'), #Rota mais curta
            '5': ('fatest','Rota Mais Rápida'),#Rota mais rapida
        }
        print("Escolha sua preferência  de rota:")
        for chave, valor in opcoes.items():
            print(f'{chave} - {valor}')
        
        while True:
            escolha=input("Digite o número da preferencia desejada:").strip()
            if escolha in opcoes:
                self.rotas= opcoes[escolha]
                print(f"Preferencia escolhida: {self.rotas}")
                break
            else:
                print("Opção inválida tente novamente.")
    def buscar_rotas(self):#função para buscar rotas da API do Google Maps
        if self.partida and self.destino:

            try:
                directions_result=self.googlemaps_cliente.directions(
                    self.partida,
                    self.destino,
                    mode='driving',#modo de viagem
                    language='pt-BR', #Linga que será exibida as informações
                    departure_time=datetime.now() #definir horario de sáida
                )
                #Extrair informações relevantes das respostas
                rota=directions_result[0] #primeira rota
                legs=rota['legs'][0]#primeira parte do percurso

                #extrair dados do percursos
                duracao=legs['duration']['text']
                distancia=legs['distance']['text']
                partida_endereco=legs['start_address']
                chegada_endereco=legs['end_address']

                #montar as  instrucoes passo a passo
                instrucoes='n/'.join([f"- {step['html_instructions']}"for step in legs ['steps']])

                #exibir todas as informações em uma única string formatada
                info=(
                    f"Distância: {distancia}\n"
                    f"Duração: {duracao}\n"
                    f"Partida: {partida_endereco}\n"
                    f"Chegada: {chegada_endereco}\n"
                    f"Duração: {duracao}\n"
                    f"Instruções passo a passo:\n {instrucoes}"
                )
                #exibir a string formatada
                print(info)

            except Exception as e:
                print(f"Erro ao buscar rota {e}")
    

        else:
                print("Partida ou destino não definidos.")


