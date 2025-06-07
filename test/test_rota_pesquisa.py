import pytest
import json


# Teste da rota de pesquisa de rotas
def test_pesquisar_rota(cliente):
    # Dados para testar a rota
    dados = {
        "origem": "São Paulo, SP",
        "destino": "Rio de Janeiro, RJ"
    }
    
    # Envia a requisição POST para a rota
    response = cliente.post('/pesquisa_rotas',data=json.dumps(dados),content_type='application/json')
    
    # Verifica o status da resposta
    assert response.status_code == 200
    
    # Verifica se os dados esperados estão presentes na resposta
    resposta_json = response.get_json()
    assert 'distancia' in resposta_json
    assert 'tempo_estimado' in resposta_json
    assert 'passos' in resposta_json

# Teste para quando não enviaremos dados
def test_pesquisar_rota_sem_dados(cliente):
    response = cliente.post('/pesquisa_rotas', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert response.json['erro'] == 'Nenhum dado enviado!'

# Teste para quando falta origem ou destino
def test_pesquisar_rota_faltando_origem_destino(cliente):
    dados = {"origem": "São Paulo, SP"}
    response = cliente.post('/pesquisa_rotas', data=json.dumps(dados), content_type='application/json')
    assert response.status_code == 400
    assert response.json['erro'] == 'Origem e Destino são obrigatorios!'

# Teste Origem e destino com valores inválidos exemplo(numero,simbolos,none)
def test_origem_destino_valores_invalidos(cliente):
    dados ={"origem":2345,
            "destino":11234
            }
    response= cliente.post('/pesquisa_rotas',
        data=json.dumps(dados),
        content_type='application/json' 
        )
    assert response.status_code == 400
    assert response.json['erro'] == "Origem e Destino deve ser string"
