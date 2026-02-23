import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path(__file__).with_name("gastos.json")

def carrregar_gastos():
    if not ARQUIVO.exists():
        return []
    
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        for g in dados:
             if "id" in g:
                g["id"] = int(g["id"])

        salvar_gastos(dados)  

        return dados
             
    except json.JSONDecodeError:
        print("gastos.json esta invalido vou começar com uma lista vazia!!")
        return []
    
def salvar_gastos(gastos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, ensure_ascii=False, indent=2)

def proximo_id(gastos):
    maior = 0
    for g in gastos:
        if g["id"] > maior:
            maior = g["id"]
            
    return maior + 1
        
def ler_valor():
    while True:
        txt = input("Valor (ex: 12.50): ").strip().replace(",", ".")
        try:
            valor = float(txt)
            if valor <= 0:
                print("Valor tem que ser maior que 0!")
                continue
            return valor

        except ValueError:
            print("Valor invalido. digite um numero (ex: 10.50)!")

def ler_data():
    while True:
        txt = input("Data (DD/MM/AAAA) ou Enter para hoje: ").strip()
        if txt == "":
            return datetime.now().strftime("%d/%m/%Y")

        try:
            datetime.strptime(txt, "%d/%m/%Y")
            return txt
        except ValueError:
            print("Data inválida. Use DD/MM/AAAA (ex: 04/08/2012)")


def editar_gasto(gastos):
    if not gastos:
        print("Nenhum gasto para editar.\n")
        return

    listar_gastos(gastos)

    txt = input("Digite o ID do gasto para editar: ").strip()
    try:
        id_editar = int(txt)
    except ValueError:
        print("ID inválido.\n")
        return

    for g in gastos:
        if int(g["id"]) == id_editar:
            print("\nDeixe vazio e aperte Enter para manter o valor atual.")
            nova_categoria = input(f'Categoria atual ({g["categoria"]}): ').strip()
            novo_valor = input(f'Valor atual ({g["valor"]:.2f}): ').strip().replace(",", ".")
            nova_data = input(f'Data atual ({g["data"]}): ').strip()

            if nova_categoria != "":
                g["categoria"] = nova_categoria

            if novo_valor != "":
                try:
                    v = float(novo_valor)
                    if v <= 0:
                        print("Valor deve ser maior que 0. Mantendo o antigo.")
                    else:
                        g["valor"] = v
                except ValueError:
                    print("Valor inválido. Mantendo o antigo.")

            if nova_data != "":
                try:
                    datetime.strptime(nova_data, "%d/%m/%Y")
                    g["data"] = nova_data
                except ValueError:
                    print("Data inválida. Mantendo a antiga.")

            salvar_gastos(gastos)
            print("✅ Gasto atualizado!\n")
            return

    print("ID não encontrado.\n")


def adiciona_gastos(gastos):
    categoria = input("categoria: ").strip()
    valor = ler_valor()
    data = ler_data()

    gasto = {
        "id": proximo_id(gastos),
        "categoria": categoria,
        "valor": valor,
        "data": data,
    }
    
    gastos.append(gasto)
    salvar_gastos(gastos)
    print("\nGastos adicionados!!")
    print("-------------------\n")

def listar_gastos(gastos):
    if not gastos:
        print("Nenhum gasto cadastrado!\n")
        return
    
    print("\n---Gastos---")
    total = 0.0
    for g in gastos:
        total += g["valor"]
        print(f'#{g["id"]} | {g["data"]} | {g["categoria"]} | {g["valor"]:.2f}')
        
    print(f"Total: R$ {total:.2f}")
    print("--------------\n")

def remover_gastos(gastos):
    if not gastos:
        print("Nenhum gasto para remover.\n")
        return

    listar_gastos(gastos)

    txt = input("Digite o ID do gasto para remover: ").strip()
    try:
        id_remover = int(txt)
    except ValueError:
        print("ID inválido. Digite um número.\n")
        return

    for i, g in enumerate(gastos):
        try:
            gid = int(g.get("id"))
        except (TypeError, ValueError):
            continue

        if gid == id_remover:
            removido = gastos.pop(i)
            salvar_gastos(gastos)
            print(f'\nRemovido: #{removido["id"]} - {removido["categoria"]} - R$ {removido["valor"]:.2f}\n')
            return

    print("ID não encontrado.\n")
    

def menu():
    gastos = carrregar_gastos()

    while True:
        print("1 - Adicionar gastos")
        print("2 - Listar gastos")
        print("3 - Remover gasto")
        print("4 - Editar gasto")
        print("0 - sair")
        op = input("Escolha: ").strip()

        if op == "1":
            adiciona_gastos(gastos)

        elif op == "2":
            listar_gastos(gastos)

        elif op == "3":
            remover_gastos(gastos)

        elif op == "4":
            editar_gasto(gastos)


        elif op == "0":
            break

        else:
            print("Opcao invalida!\n")


if __name__ == "__main__":
    menu()

