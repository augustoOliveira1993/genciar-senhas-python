import sqlite3

conn = sqlite3.connect('gerencia_senha.db')
cursor = conn.cursor()

# Caso nao tenha o banco
# cursor.execute("""DROP TABLE gerencia_senha""")

def criar_tabela():
    cursor.execute("""CREATE TABLE IF NOT EXISTS gerencia_senha (
                      id_alter INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      service TEXT,
                      username TEXT,
                      password TEXT
                  )
             """)
    print('Tabela criada com sucesso!')


MASTER_PASSWORD = "123456"

# senha = input("Insira sua senha master: ")
senha = '123456'
if senha != MASTER_PASSWORD:
    print('Senha invalida!.. Encerrando...')
    exit()

def menu():
    print("*******************************")
    print("* [i]: inserir nova senhas      *")
    print("* [l]: lista de serviços salvos *")
    print("* [a]: Alterar senha            *")
    print("* [d]: Remover servico por id   *")
    print("* [r]: recuperar uma senha      *")
    print("* [s]: sair                     *")
    print("*******************************")

def get_pasword(service):
    cursor.execute(f"""
        SELECT  username, password FROM gerencia_senha
        WHERE service='{service}'""")
    if cursor.rowcount == 0:
        print("Serviço nao cadastrado (use 'l' para verificar os serviços).")
    else:
        result = cursor.fetchall()
        for r in result:
            user, senha = r
            print()
            print('###'*10)
            print(f'Usuario: {user}\nSenha: {senha}')
            print('###'*10)
            print()

def alterar_senha(service):
    new_senha = ''
    id_alter = ''
    cursor.execute(f"""
        SELECT id_alter, username, password FROM gerencia_senha
        WHERE service='{service}'""")
    if cursor.rowcount == 0:
        print("Serviço nao cadastrado (use 'l' para verificar os serviços).")
    else:
        result = cursor.fetchall()
        for r in result:
            id_at, user, senha = r
            print(f'A senha é {senha}.')
            id_alter = id_at
    new_senha = input('Nova Senha: ')
    cursor.execute(f"""
        UPDATE gerencia_senha
        SET password = '{new_senha}'
        WHERE id_alter = {id_alter}
        """)
    conn.commit()
        
    
def insert_password(service, username, password):
    sql = f"INSERT INTO gerencia_senha (service, username, password) VALUES ('{service}', '{username}', '{password}')"
    cursor.execute(sql)
    conn.commit()
    
def show_services():
    print('\n-=-=-= SERVIÇOS =-=-=-=-')
    sql = 'SELECT * FROM gerencia_senha'
    result = cursor.execute(sql)
    for r in result:
        id_s, service, username, password = r
        print(f'ID: {id_s} | {service}: {username}')
    print('-=-'*8)
    print()
    
def remover_por_id(id_ser: int):
    cursor.execute(f"""DELETE FROM gerencia_senha WHERE id_alter={id_ser}""")
    conn.commit()
    print()
    print('###'*8)
    print(f'Serviço deletado com sucesso!')
    print('###'*8)
    print()

def mostrar_por_id(id_serv: int):
    deletado = cursor.execute(f"""SELECT id_alter, service FROM gerencia_senha WHERE id_alter={id_serv}""")
    return list(deletado)

# cursor.execute("""INSERT INTO gerencia_senha (service, username, password) VALUES ('GitHub', 'gutim160@gmail.com', '88146347')""")
while True:
    # criar_tabela()
    menu()
    op = str(input('O que voçe deseja fazer? ')).upper()
    if op not in ['I','L','R','S', 'A', 'D']:
        print('Opçao invalida')
        continue
     
    if op == 'S':
        break
        
    if op == 'I':
        service = input('Qual o nome do serviço? ').upper()
        username = input('Qual o nome do usuario? ')
        password = input('Qual a senha? ')
        insert_password(service, username, password)
        
    if op == 'L':
        show_services()
        
    if op == 'R':
        service = input('Qual o serviço para o qual quer a senha? ').strip().upper()
        get_pasword(service)

    if op == 'A':
        service = input('De qual servico deseja alterar senha: ').strip().upper()
        alterar_senha(service)

    # TODO: Adicionar fucionalidade
    if op == 'D':
        id_serv = int(input('Qual ID deseja Excluir: '))
        if not type(id_serv) != int:
            remover_por_id(id_serv)
        else:
            print('Tipo de dados incorreto!, Favor digitar inteiro(int).')
conn.close()
