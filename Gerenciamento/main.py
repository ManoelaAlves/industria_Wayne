from db import conexao

# Criando um cursor para executar os comandos SQL
cursor = conexao.cursor()

# Inserindo dados na tabela 'usuarios'
#Admministrador 3, gerente 2, funcionário 1
cursor.execute("""
    INSERT INTO usuarios (nome, senha, type_acesso) VALUES 
    ('Manoela Bastos', 'senha_manoela', 3),
    ('Bruno Foloni', 'senha_bruno', 2),
    ('José ricardo', 'senha_jose', 1)
""")

# Inserindo dados na tabela 'areas'
cursor.execute("""
    INSERT INTO area_restrita (nome_area, type_acesso_necessario) VALUES 
    ('Sala de Controle', 2),
    ('Laboratório de teste', 1)
""")

conexao.commit()

# Fechando a conexão
cursor.close()
conexao.close()
