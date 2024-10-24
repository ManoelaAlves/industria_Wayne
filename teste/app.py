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
            host='127.0.0.1',  
            user='root',
            password='M@21Tb30',  
            database='bd_projeto' 
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

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html') 
############################################################################################################################################
@app.route('/recursos', methods=['GET'])
def recursos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    # Seleciona todos os recursos
    cursor.execute("SELECT * FROM recursos")
    recursos = cursor.fetchall()
    
    return render_template('recursos.html', recursos=recursos)
@app.route('/add-recurso', methods=['POST'])
def add_recurso():
    nome = request.form.get('nome')
    tipo = request.form.get('tipo')
    status = request.form.get('status')
    descricao = request.form.get('descricao')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Add the new line on MYSQL
    query = "INSERT INTO recursos (nome, tipo, status, descricao) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nome, tipo, status, descricao))
    conexao.commit()

    return redirect('/recursos')

# Rota para editar recurso (POST)
@app.route('/edit-recurso/<int:id>', methods=['POST'])
def edit_recurso(id):
    nome = request.form.get('nome')
    tipo = request.form.get('tipo')
    status = request.form.get('status')
    descricao = request.form.get('descricao')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Atualizar o recurso no banco de dados
    query = "UPDATE recursos SET nome = %s, tipo = %s, status = %s, descricao = %s WHERE idrecursos = %s"
    cursor.execute(query, (nome, tipo, status, descricao, id))
    conexao.commit()

    return redirect('/recursos')

# Rota para excluir recurso (POST)
@app.route('/delete-recurso/<int:id>', methods=['POST'])
def delete_recurso(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Excluir o recurso do banco de dados
    query = "DELETE FROM recursos WHERE idrecursos = %s"
    cursor.execute(query, (id,))
    conexao.commit()

    return redirect('/recursos')

############################################################################################################################################

@app.route('/login', methods=['GET'])
def voltar():
    return render_template('login.html')
@app.route('/falha')
def falha():
    return render_template('falha.html')

# Especificar o método POST para a rota /login
@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    area = request.form.get('area')
    
    print(nome)
    print(senha)
    print(area)
    
    usu_aut = autenticar(nome,senha)
    # Verificar se o usuário foi encontrado
    if usu_aut == True:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute('SELECT idusuarios FROM usuarios WHERE nome = %s AND senha = %s', (nome, senha))
        usuario = cursor.fetchone()
        if usuario is not None:
            id = usuario['idusuarios']  # Acessa o valor do 'idusuarios'
            if verificar(id, area):
                print(f"ID do usuário: {id} tem acesso à área {area}")
                return redirect('/sucesso')  # Redirecionar para a página autorizada
            else:
                print(f"ID do usuário: {id} NÃO tem acesso à área {area}")
                return redirect('/falha')  # Redireciona de volta ao login por falta de permissão
        else:
            # Caso o id não seja encontrado, retorne ao login
            return redirect('/falha')  # Redireciona de volta para a página de login
    else:
        # Usuário não encontrado, redireciona para a página de login com erro
        return redirect('/falha')
    
    
    
#Autenticando se o nome e senha estão presentes no banco de dados
def autenticar(nome, senha):
    if nome and senha:
        # Conectar ao banco de dados
        conexao = conectar_banco()
        print(conexao)
        cursor = conexao.cursor(dictionary=True)

        # Consulta SQL para verificar se o usuário existe
        query = "SELECT * FROM usuarios WHERE nome = %s AND senha = %s"
        cursor.execute(query, (nome, senha))
        usuario = cursor.fetchone()
        
        if usuario:
            return True
        else:
            return False

    # Caso os campos não sejam preenchidos corretamente
    return redirect('/')

#Verificando qual o nível de acesso que o usuário informado possui, e assim verificando o acesso a área, precisa de acesso as duas tabelas
def verificar(id, area):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Consulta para verificar o nível de acesso necessário para a área
    cursor.execute("SELECT type_acesso_necessario FROM area_restrita WHERE nome_area = %s", (area,))
    dados_area = cursor.fetchone()

    # Consulta para verificar o nível de acesso do usuário
    cursor.execute("SELECT type_acesso FROM usuarios WHERE idusuarios = %s", (id,))
    dados_usuario = cursor.fetchone()

    # Se ambos os resultados existirem, comparar os níveis de acesso
    if dados_area and dados_usuario:
        if dados_usuario['type_acesso'] >= dados_area['type_acesso_necessario']:
            return True  # Usuário tem acesso
    return False  # Usuário não tem acesso

if __name__ == '__main__':
    app.run(debug=True)
