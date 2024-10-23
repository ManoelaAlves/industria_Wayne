from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
# Variável de segurança
app.config['SECRET_KEY'] = 'MANOELABASTOS'

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',  # Você pode usar 'localhost' ou '127.0.0.1'
            user='root',
            password='M@21Tb30',  # Verifique se essa senha está correta
            database='bd_projeto'  # Certifique-se que o banco de dados 'bd_projeto' existe
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida!")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return e


@app.route('/')
def home():
    return render_template('login.html')

# Especificar o método POST para a rota /login
@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    area = request.form.get('area')
    
    print(nome)
    print(senha)
    print(area)

    #    # Verifica se todos os campos foram preenchidos
    if nome and senha:
        # Conectar ao banco de dados
        conexao = conectar_banco()
        print(conexao)
        cursor = conexao.cursor(dictionary=True)

        # Consulta SQL para verificar se o usuário existe
        query = "SELECT * FROM usuarios WHERE nome = %s AND senha = %s"
        cursor.execute(query, (nome, senha))
        usuario = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conexao.close()

        # Verificar se o usuário foi encontrado
        if usuario:
            # Sucesso no login, redireciona para a página inicial ou área protegida
            return redirect('/')  # Mude para a página que você deseja redirecionar após o login bem-sucedido
        else:
            # Usuário não encontrado, redireciona para a página de login com erro
            return redirect('/')

    # Caso os campos não sejam preenchidos corretamente
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
