# Rota Rapida.

# Descrição

  Este programa permite o usuário traçar rotas entre dois locais. Levando
em consideração preferência de rotas e trânsito.

# 📌 Banco de Dados - MySQL.
### O banco de dados utilizado no projeto é MySQL, responsável por armazenar as informações das pesquisas de rotas dos usuários..
#### 📁 Tabelas do Banco de Dados.
#### Tabela: usuario.
Armazena os usuários que utilizam o sistema, sem necessidade de autenticação.

|Campo|Tipo de Dado|Restrição|Descrição|
|-----|-------------|--------|---------|
|`id`|INTEGER|PRIMARY KEY AUTOINCREMENT|Identificador único do usuário|
|`nome`|VARCHAR(100)|NOT NULL|nome do usuario|
