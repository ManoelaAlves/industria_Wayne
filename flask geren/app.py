from flask import Flask, request, jsonify
from db import conexao

app = Flask(__name__)

# Autenticação do usuário
def autenticar(nome, senha):
    comando = conexao
    cursor = comando.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
    usuario = cursor.fetchone()

    if not usuario or senha != usuario['senha']:
        return None
    return usuario

# Verificação do nível de acesso
def verificar(nome, area):
    comando = conexao
    cursor = comando.cursor(dictionary=True)

    cursor.execute("SELECT type_acesso_necessario FROM area_restrita WHERE nome_area = %s", (area,))
    dados_area = cursor.fetchone()

    cursor.execute("SELECT type_acesso FROM usuarios WHERE nome = %s", (nome,))
    dados_usuario = cursor.fetchone()

    if dados_area and dados_usuario:
        if dados_usuario['type_acesso'] >= dados_area['type_acesso_necessario']:
            return True
    return False

# Rota para processar o login e verificação de acesso
@app.route('/acesso', methods=['POST'])
def acesso():
    dados_recebidos = request.json
    nome = dados_recebidos.get('nome')
    senha = dados_recebidos.get('senha')
    area = dados_recebidos.get('area')

    # Autenticar o usuário
    usuario = autenticar(nome, senha)
    if usuario:
        # Verificar o nível de acesso
        if verificar(nome, area):
            return jsonify({"mensagem": "Acesso permitido"})
        else:
            return jsonify({"mensagem": "Acesso negado: Permissão insuficiente"})
    else:
        return jsonify({"mensagem": "Usuário ou senha inválidos"})

if __name__ == '__main__':
    app.run(debug=True)
