import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS gastos (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               categoria TEXT NOT NULL,
               valor FLOAT NOT NULL,
               data TEXT NOT NULL,
               descricao TEXT
               )""");


def inserir_gastos():
    categoria = input("Categoria: ").strip()
    valor = input("Valor: ").strip()
    data = ler_data()
    descricao = input("descricao (opcional): ").strip()

    cursor.execute(
        "INSERT INTO gastos (categoria, valor, data, descricao) VALUES (?, ?, ?, ?)",
        (categoria, valor, data, descricao)
    )

    conexao.commit()
    
def editar_gastos():
        txt = input("ID: ").strip()

        if not txt:
            print("Você não digitou um ID.")
            return
        
        id_alvo = int(txt)

        cursor.execute(
        "SELECT categoria, valor, data, descricao FROM gastos WHERE id=?",
        (id_alvo,)
        )

        atual = cursor.fetchone()
        if atual is None:
            print("ID não encontrado.")
            return

        cat_atual, valor_atual, data_atual, desc_atual = atual

        cat = input(f"Categoria ({cat_atual}): ").strip() or cat_atual
        valor_txt = input(f"Valor ({valor_atual}): ").strip()
        valor = float(valor_txt.replace(",", ".")) if valor_txt else valor_atual
        data = input(f"Data ({data_atual}): ").strip() or data_atual
        desc = input(f"Descrição ({desc_atual}): ").strip() or desc_atual

        cursor.execute(
        "UPDATE gastos SET categoria=?, valor=?, data=?, descricao=? WHERE id=?",
        (cat, valor, data, desc, id_alvo)
        )

        conexao.commit()
    
def deletar_gastos():
    txt = input("Digite o id para DELETAR: ").strip()
    try:
        id_alvo = int(txt)
    except:
        print("Id invalido!")
        return

    cursor.execute("DELETE FROM gastos WHERE id = ?", (id_alvo,))

    if cursor.rowcount == 0:
        print('id nao encontrado!')

    else:
        print(f'ID {id_alvo} deletado!')

    conexao.commit()


def ler_data():
    txt = input("Data (DD/MM/AAAA): ").strip()
    return txt


def ver_gastos():
    cursor.execute("""SELECT * FROM gastos""")
    contas = cursor.fetchall()

    for conta in contas:
        id, categoria, valor, data, descricao = conta
        print(f"""id: {id}
    categoria: {categoria}
    valor: {valor}
    data: {data}
    descricao: {descricao} \n""")
        
    conexao.commit()


def menu():
    while True:
        print('\n1 - ver gastos')
        print('2 - adicionar gastos')
        print('3 - Remover gastos')
        print('4 - editar gastos')
        print('0 - sair')
        op = input('Escolha uma opcao: ').strip()
        
        if op == '1':
            ver_gastos()
        elif op == '2':
            inserir_gastos()
        elif op == '3':
            deletar_gastos()
        elif op == '4':
            editar_gastos()
        elif op == '0':
            break
        else:
            print("Opcao invalida!")

menu()

conexao.commit()