import pytest
import json

#Testar se a rota retorna erro quando nenhum filtro é enviado

def test_rota_sem_nehum_filtro(cliente):
    dados={}
    resposta= cliente.post(
        "/filtros_pesquisa", 
        data=json.dumps(dados),
        content_type='application/json')
    #verifica se o status code da aplicação é igual 400
    assert resposta.status_code == 400
    #verificar a resposta.
    assert resposta.get_json() == {"erro":"Nenhum filtro aplicado!"}
def test_sem_origem_e_destino(cliente):
    dados={
        "modo_de_transporte":"driving",
    }
    resposta= cliente.post(
        "/filtros_pesquisa",json=dados
    )
    #conferindo se o status da aplicação é 400
    assert resposta.status_code == 400
    assert resposta.get_json() == {'erro':'Os campos origem e destino são obrigatórios.'}
def test_modo_trasport_invalido(cliente):
    dados={
        "origem": "Rua A",
        "destino": "Rua B",
        "modo_transporte":"carro"
    }
    resposta=cliente.post("/filtros_pesquisa",json=dados)
    #coferindo o status da aplicação
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro":f"Modo e transporte  inválido! Escolha entre ['driving', 'walking', 'bicycling', 'transit']"}


def test_campos_booleanos_recebendo_valores_invalidos(cliente): 
    dados={ "origem": "Rua A", 
           "destino": "Rua B", 
           "modo_transporte": "driving", 
           "evitar_rodovias": "sim" 
           } 
    resposta= cliente.post("filtros_pesquisa",json=dados)
    assert resposta. status_code == 400
    assert resposta.get_json() == {"erro":"Valores invalidos"}
    

