from db import conexao
#import cgi
import json
import sys

#Autenticando se o nome e senha estão presentes no banco de dados
def autenticar(nome, senha):
    #Estabelecendo o acesso ao banco de dados
    comando = conexao
    #o cursor vai retornar os resultados como dicionário
    cursor = comando.cursor(dictionary=True)
    #Executando o comando 
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
    #Método
    usuario = cursor.fetchone()
    #Condição de autenticação 
    if not usuario or senha != usuario['senha']:
        return None
    return usuario

#Verificando qual o nível de acesso que o usuário informado possui, e assim verificando o acesso a área, precisa de acesso as duas tabelas
def verificar(nome, area):
    #Estabelecendo o acesso ao banco de dados
    comando = conexao
    #o cursor vai retornar os resultados como dicionário
    cursor = comando.cursor(dictionary=True)
    #Executando o comando 
    cursor.execute("SELECT type_acesso_necessario FROM area_restrita WHERE nome_area = %s", (area,))
    #Método
    dados_area = cursor.fetchone()
    # Executando a consulta para obter o nível de acesso do usuário
    cursor.execute("SELECT type_acesso FROM usuarios WHERE nome = %s", (nome,))
    dados_usuario = cursor.fetchone()  
    #Condição de autenticação 
    #Verifica o que o que o banco de dados retornou
    if dados_area and dados_usuario:  
    # Compara o nível de acesso do usuário com o nível de acesso requerido para a área (no banco de dados essas variáveis foram declaradas como INT)
        if dados_usuario['type_acesso'] >= dados_area['type_acesso_necessario']:
            #True se tiver permissão concedida
            return True  
    return False

# Puxando os dados do formulário
try:
    dados_recebidos = json.load(sys.stdin)
except json.JSONDecodeError:
    print(json.dumps({"mensagem": "Erro ao processar os dados recebidos."}))
    sys.exit(1)

# Autenticar o usuário, chamando a função e pasasndo os parãmetros
usuario = autenticar(dados_recebidos['nome'], dados_recebidos['senha'])

if usuario:
    # Verificar se o usuário tem acesso à área solicitada
    resultado_acesso = verificar(usuario, dados_recebidos['area'])
else:
    resultado_acesso = "Usuário ou senha inválidos."

# Retornar a resposta em formato JSON
resposta = {"mensagem": resultado_acesso}
print(json.dumps(resposta))
 