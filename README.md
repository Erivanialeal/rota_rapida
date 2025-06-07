# Rota Rapida.

# Descrição

  Este programa permite o usuário traçar rotas entre dois locais. Levando
em consideração preferência de rotas e trânsito.

<<<<<<< HEAD
# 📌 Banco de Dados - MySQL.
### O banco de dados utilizado no projeto é MySQL, responsável por armazenar as informações das pesquisas de rotas dos usuários..
#### 📁 Tabelas do Banco de Dados.
#### Tabela: usuario.
Armazena os usuários que utilizam o sistema, sem necessidade de autenticação.

|**Coluna**|**Tipo de Dado**|**Restrição|Descrição**|
|-----|-------------|--------|---------|
|`id`|INTEGER|PRIMARY KEY AUTOINCREMENT|Identificador único do usuário|
|`nome`|VARCHAR(100)|NOT NULL|nome do usuario|

### Tabela: pesquisa.
Armazena informações sobre as pesquisas de rota realizadas pelos usuários.
### Relacionamento:
`usuario_id`: Chave estrangeira que liga a pesquisa a um usuário na tabela `usuario`.

| **Coluna**      | **Tipo de Dado**       | **Restrições**  | **Descrição** |
|----------------|----------------------|---------------|--------------|
| `id`          | `Integer`             | `PK`, `AutoIncrement` | Identificador único da pesquisa. |
| `usuario_id`  | `Integer`             | `FK(usuario.id)`, `NOT NULL` | Referência ao usuário que realizou a pesquisa. |
| `origem`      | `String(300)`         | `NOT NULL`     | Local de partida da pesquisa. |
| `destino`     | `String(300)`         | `NOT NULL`     | Destino da pesquisa. |
| `data_e_hora` | `DateTime`            | `Default=datetime.utcnow`, `NOT NULL` | Data e hora em que a pesquisa foi feita. |

### Tabela: filtros.
A tabela `filtros` armazena os filtros disponíveis para o usuário.
### Relacionamentos:
`pesquisa_id`´: Chave estrangeira que vincula o filtro à pesquisa correspondente na tabela `pesquisa`. Quando a pesquisa é excluída, os filtros relacionados são excluídos automaticamente devido à restrição `ON DELETE CASCADE`.
| **Coluna**                             | **Tipo de Dado**                                | **Restrições**                           | **Descrição** |
|----------------------------------------|------------------------------------------------|----------------------------------------|---------------|
| `id`                                   | `Integer`                                      | `PK`, `AutoIncrement`                   | Identificador único do filtro. |
| `pesquisa_id`                          | `Integer`                                      | `FK(pesquisa.id)`, `NOT NULL`, `ON DELETE CASCADE` | Referência à pesquisa associada. Caso a pesquisa seja excluída, os filtros relacionados serão automaticamente excluídos. |
| `modo_transporte`                      | `Enum('carro', 'moto', 'bicicleta', 'ônibus', 'a pé')` | `NOT NULL`                              | Modo de transporte escolhido para a pesquisa de rota. |
| `evitar_rodovias`                      | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário deseja evitar rodovias na pesquisa. |
| `evitar_transito_pesado`               | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário deseja evitar áreas com trânsito pesado. |
| `evitar_pedagios`                      | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário deseja evitar pedágios. |
| `evitar_estradas_nao_pavimentadas`     | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário deseja evitar estradas não pavimentadas. |
| `rota_mais_curta`                      | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário prefere a rota mais curta. |
| `rota_mais_longa`                      | `Boolean`                                      | `NOT NULL`, `Default=False`              | Indica se o usuário prefere a rota mais longa. |

### Tabela: historico_pesquisa.
Armazena todo o historico de pesquisa de um determinado usuário.
### Relacionamentos:
`usuario_id`: Chave estrangeira que vincula o histórico à tabela `usuario`.
`pesquisa_id`: Chave estrangeira que vincula o histórico à tabela `pesquisa`´. Quando a pesquisa é excluída, o histórico relacionado também é excluído devido à restrição `ON DELETE CASCADE`.

| **Coluna**                             | **Tipo de Dado**                                | **Restrições**                           | **Descrição** |
|----------------------------------------|------------------------------------------------|----------------------------------------|---------------|
| `id`                                   | `Integer`                                      | `PK`, `AutoIncrement`                   | Identificador único do histórico de pesquisa. |
| `usuario_id`                           | `Integer`                                      | `FK(usuario.id)`, `NOT NULL`            | Referência ao usuário que realizou a pesquisa. |
| `pesquisa_id`                          | `Integer`                                      | `FK(pesquisa.id)`, `NOT NULL`, `ON DELETE CASCADE` | Referência à pesquisa realizada. Caso a pesquisa seja excluída, o histórico relacionado será automaticamente excluído. |
| `data_pesquisa`                        | `DateTime`                                     | `Default=datetime.utcnow`, `NOT NULL`    | Data e hora em que a pesquisa foi realizada. |
| `vezes_pesquisada`                     | `Integer`                                      | `NOT NULL`, `Default=1`                  | Número de vezes que a pesquisa foi realizada. |

### Tabela: resultado_pesquisa.
Armazena os resultados de todas as pesquisas feita por um determinado usuário.
### Relacionamento:
`pesquisa_id`: Chave estrangeira que vincula o resultado à pesquisa na tabela `pesquisa`.
| **Coluna**                             | **Tipo de Dado**                                | **Restrições**                           | **Descrição** |
|----------------------------------------|------------------------------------------------|----------------------------------------|---------------|
| `id`                                   | `Integer`                                      | `PK`, `AutoIncrement`                   | Identificador único do resultado da pesquisa. |
| `pesquisa_id`                          | `Integer`                                      | `FK(pesquisa.id)`, `NOT NULL`           | Referência à pesquisa associada. |
| `rota`                                 | `String(300)`                                  | `NOT NULL`                              | JSON contendo detalhes da rota (ex: pontos de passagem, nome das vias, etc.). |
| `distancia`                            | `Float`                                        | `NOT NULL`                              | Distância total da rota em quilômetros. |
| `duracao`                              | `Integer`                                      | `NOT NULL`                              | Tempo estimado para percorrer a rota, em minutos. |
| `criado_em`                            | `DateTime`                                     | `Default=datetime.utcnow`, `NOT NULL`    | Data e hora em que o resultado foi armazenado. |



