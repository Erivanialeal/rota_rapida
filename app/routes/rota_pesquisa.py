from flask import Blueprint,jsonify,request
from app.config import Config
import requests
import os
from sqlalchemy import desc




# Criar um Blueprint para organizar as rotas
pesquisa_bp=Blueprint("pesquisa",__name__)

@pesquisa_bp.route("/pesquisa_rotas",methods=['POST'])

def pesquisar_rota():
    API_KEY=Config.API_KEY #obter a chave corretamente
    if not API_KEY:
        return jsonify({'erro':'API_KEY não encontrada!'}),500
    #fazendo a requisição
    dados=request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado!'}), 400
    
    origem=dados.get('origem')
    destino=dados.get('destino')
    if not origem or not destino:
        return jsonify({'erro':'Origem e Destino são obrigatorios!'}),400
    
    url=f"https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&key={API_KEY}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Garante que erros HTTP sejam tratados
        dados_resposta = resposta.json()

        # Verificando se há rotas na resposta
        if "routes" not in dados_resposta or not dados_resposta["routes"]:
            return jsonify({'erro': 'Nenhuma rota encontrada!'}), 404
        
        dados_formatados={
            "distancia":dados_resposta['routes'][0]['legs'][0]['distance']['text'],
            "tempo_estimado":dados_resposta['routes'][0]['legs'][0]['duration']['text'],
            "passos":[
                {
                     "descricao": passo["html_instructions"],
                    "distancia": passo["distance"]["text"]
                }
                for passo in dados_resposta['routes'][0]['legs'][0]['steps']
            ]
        }
        return jsonify(dados_formatados)

    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'Erro ao consultar a API.', 'detalhes': str(e)}), 500
    
@pesquisa_bp.route('/filtros_pesquisa', methods=['POST'])  
def filtros():
    API_KEY=Config.API_KEY 
    if not API_KEY:
        return jsonify({'erro':'API_KEY não encontrada!'}),500
    
    dados=request.get_json() #obter os dados json enviado na requisição

    if not dados:
        return jsonify({'erro': 'Nenhum filtro aplicado!'}), 400
    #recebendo o modo de transporte
    origem = dados.get("origem")
    destino = dados.get("destino")
    modo_transporte=dados.get('modo_transporte', 'driving')
    #recebendo os filtros com booleanos
    evitar_rodovias=dados.get('evitar_rodovias', False)
    evitar_transito_pesado=dados.get('evitar_transito',False)
    evitar_pedágios=dados.get('evitar_transito', False)
    evitar_estradas_nao_pavimentadas=dados.get('evitar_estradas_nao_pavimentadas', False)
    rota_mais_curta=dados.get('rota_mais_curta', False)
    rota_mais_longa=dados.get('rota_mais_longa', False)

    #criando parâmentros da API de mapas
    parametros={
        "mode": modo_transporte,
        "avoid": []
    } 
    if evitar_rodovias:
        parametros['avoid'].append('highways')
    if evitar_transito_pesado:
        parametros['avoid'].append('traffic')
    if evitar_pedágios:
        parametros['avoid'].append('tolls')
    if evitar_estradas_nao_pavimentadas:
        parametros['avoid'].append('unpaved')
    if rota_mais_curta and not rota_mais_longa:
         parametros["optimize"] = "shortest"
    elif rota_mais_longa and not rota_mais_curta:
        parametros["optimize"] = "longest"
    # Adicionando chave de API e outros parâmetros obrigatórios
    parametros["origin"] = origem
    parametros["destination"] = destino
    parametros["key"] = API_KEY 
    URL_API_MAPAS =  "https://maps.googleapis.com/maps/api/directions/json"

    # Fazendo a requisição para a API de mapas
    resposta = requests.get(URL_API_MAPAS, params=parametros)
    if resposta.status_code != 200:
        return jsonify({'erro': 'Falha na requisição para a API de Mapas', 'detalhes': resposta.json()}), 500
     # Retornando a resposta real da API
    return jsonify(resposta.json())

@pesquisa_bp.route('/salvar_historico_pesquisa/<int:usuario_id>',methods=['POST'])
def salvar_historico_de_pesquisa(usuario_id):
    from app.models import Usuario,HistoricoPesquisa,Pesquisa
    from app import db
    import requests
    #verificar se o usuario existe
    usuario=Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"ero":"Usuario não encontrado"}),404 #não encontrado
    # Obtém os dados da requisição
    dados_requisicao = request.get_json()
    origem = dados_requisicao.get('origem')
    destino = dados_requisicao.get('destino')
    if not origem or not destino:
        return jsonify({"erro": "Origem e destino são obrigatórios"}), 400
    # Faz requisição para a API externa
    api_key = Config.API_KEY
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&key={api_key}"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        return jsonify({"erro": "Erro ao obter os dados da API externa"}), 502

    dados = resposta.json()

    if "routes" not in dados or not dados["routes"]:
        return jsonify({"erro": "Nenhuma rota encontrada"}), 404

    # Salva a pesquisa
    nova_pesquisa = Pesquisa(
    usuario_id=usuario_id,  # Certifique-se de passar um usuário válido
    origem=origem,
    destino=destino
)

    db.session.add(nova_pesquisa)
    db.session.commit()

    # Salva o histórico de pesquisa
    nova_pesquisa_historico = HistoricoPesquisa(usuario_id=usuario_id, pesquisa_id=nova_pesquisa.id)
    db.session.add(nova_pesquisa_historico)
    db.session.commit()

    return jsonify({"mensagem": "Histórico de pesquisa salvo com sucesso"}), 201
@pesquisa_bp.route('/adicionar_usuario',methods=['POST'])
def usuario():
    from app import db
    from app.models import Usuario
    dados=request.get_json() #Obtendo os dados da requisição
    if not dados:
        return jsonify({"erro":"Nenhum dado encontrado!"}),400
    nome = dados.get("nome")
    if not nome:
        return jsonify({"mensagem":"Nome do usuário não fornecido."}),400
    #criando o usuario
    novo_usuario=Usuario(nome=nome)
    
    try:
        db.session.add(novo_usuario) #adiciona o usuario a sessão
        db.session.commit() #Salva no banco
        return jsonify({"mensagem": "Usuário adicionado com sucesso!", "id": novo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()  # Cancela qualquer erro no banco
        return jsonify({"erro": f"Erro ao salvar usuário: {str(e)}"}), 500

@pesquisa_bp.route('/resultado_de_historico/<int:usuario_id>',methods=['GET'])
def resultado_de_historico(usuario_id):
    from app.models import Usuario,Pesquisa,HistoricoPesquisa
    #Buscar usuario no banco
    usuario=Usuario.query.get(usuario_id)
    print(usuario)
    if not usuario:
        return jsonify({"Erro":"Usuario não encontrado"}),404
    #Buscar a ultima pesquisa no banco de dados
    ultima_pesquisa=HistoricoPesquisa.query.filter_by(usuario_id=usuario_id).order_by(HistoricoPesquisa.data_pesquisa.desc()).first()
    print(ultima_pesquisa)
    if not ultima_pesquisa:
        return jsonify({"Erro":"Nenhuma pesquisa encontrada para este usuario"}),404
    return jsonify({
        "id":ultima_pesquisa.id,
        "usuario_id":ultima_pesquisa.usuario_id,
        "pesquisa_id":ultima_pesquisa.pesquisa_id,
        "data_pesquisa":ultima_pesquisa.data_pesquisa,
        "vezes_pesquisada":ultima_pesquisa.vezes_pesquisada
    }),200

