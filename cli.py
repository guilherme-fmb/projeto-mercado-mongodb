from datetime import datetime

class CLI:
    def __init__(self, db_operations):
        self.db_operations = db_operations

    def exibir_produtos(self):
        produtos = self.db_operations.buscar_produtos()
        if not produtos:
            print("\nNenhum produto encontrado.")
            return
        print("\nProdutos disponíveis:")
        for produto in produtos:
            print(f"- Código: {produto['codigo']} | Nome: {produto['nome']} | Preço: R$ {produto['preco']:.2f}")

    def realizar_compra(self):
        print("\nIniciando uma nova compra:")
        produtos = self.db_operations.buscar_produtos()
        if not produtos:
            print("Nenhum produto disponível para compra.")
            return

        carrinho = []
        while True:
            self.exibir_produtos()
            codigo = input("\nDigite o código do produto para adicionar ao carrinho (ou 'fim' para finalizar): ").strip()
            if codigo.lower() == 'fim':
                break

            produto = next((p for p in produtos if p['codigo'] == codigo), None)
            if produto:
                carrinho.append(produto)
                print(f"Produto '{produto['nome']}' adicionado ao carrinho.")
            else:
                print("Produto não encontrado. Tente novamente.")

        if not carrinho:
            print("Compra cancelada. Nenhum item no carrinho.")
            return

        detalhes_compra = self.db_operations.registrar_compra(carrinho)
        print("\nCompra registrada com sucesso!")
        print(f"Total: R$ {detalhes_compra['total']:.2f}")
        print("Itens comprados:")
        for item in detalhes_compra['produtos']:
            print(f"- {item['nome']} | Preço: R$ {item['preco']:.2f}")

    def buscar_por_data(self):
        data_str = input("\nDigite a data (DD-MM-YYYY) para buscar compras: ").strip()
        try:
            data = datetime.strptime(data_str, "%d-%m-%Y")
        except ValueError:
            print("Data inválida! Use o formato YYYY-MM-DD.")
            return

        compras = self.db_operations.buscar_compras_por_data(data)
        if not compras:
            print("\nNenhuma compra encontrada para esta data.")
            return

        print("\nCompras encontradas:")
        for compra in compras:
            print(f"- ID: {compra['_id']} | Total: R$ {compra['total']:.2f} | Data: {compra['data_hora']}")
            for produto in compra['produtos']:
                print(f"  Produto: {produto['nome']} | Preço: R$ {produto['preco']:.2f}")

    def buscar_por_id(self):
        compra_id = input("\nDigite o ID da compra: ").strip()
        compra = self.db_operations.buscar_compra_por_id(compra_id)
        if not compra:
            print("Compra não encontrada.")
            return

        print(f"\nCompra encontrada:")
        print(f"- ID: {compra['_id']} | Total: R$ {compra['total']:.2f} | Data: {compra['data_hora']}")
        for produto in compra['produtos']:
            print(f"  Produto: {produto['nome']} | Preço: R$ {produto['preco']:.2f}")

    def deletar_compra_por_id(self):
        compra_id = input("\nDigite o ID da compra a ser deletada: ").strip()
        sucesso = self.db_operations.deletar_compra_por_id(compra_id)
        if sucesso:
            print("Compra deletada com sucesso.")
        else:
            print("Erro: Compra não encontrada ou ID inválido.")

    def adicionar_produto(self):
        print("\nAdicionar novo produto:")
        codigo = input("Código: ").strip()
        nome = input("Nome: ").strip()
        try:
            preco = float(input("Preço: ").strip())
        except ValueError:
            print("Preço inválido! Operação cancelada.")
            return
        if self.db_operations.adicionar_produto(codigo, nome, preco):
            print("Produto adicionado com sucesso!")
        else:
            print("Erro: Produto com este código já existe.")

    def exibir_todas_compras(self):
        compras = self.db_operations.exibir_todas_compras()
        if not compras:
            print("\nNenhuma compra registrada.")
            return
        print("\nLista de todas as compras:")
        for compra in compras:
            print(f"- ID: {compra['_id']} | Total: R$ {compra['total']:.2f} | Data: {compra['data_hora']}")
            for produto in compra['produtos']:
                print(f"  Produto: {produto['nome']} | Preço: R$ {produto['preco']:.2f}")

    def menu(self):
        while True:
            print("\n=== Supermercado ===")
            print("1. Exibir produtos")
            print("2. Realizar compra")
            print("3. Buscar compras por data")
            print("4. Buscar compra por ID")
            print("5. Deletar compra por ID")
            print("6. Adicionar novo produto")
            print("7. Exibir todas as compras")
            print("8. Sair")

            opcao = input("Escolha uma opção: ").strip()
            if opcao == '1':
                self.exibir_produtos()
            elif opcao == '2':
                self.realizar_compra()
            elif opcao == '3':
                self.buscar_por_data()
            elif opcao == '4':
                self.buscar_por_id()
            elif opcao == '5':
                self.deletar_compra_por_id()
            elif opcao == '6':
                self.adicionar_produto()
            elif opcao == '7':
                self.exibir_todas_compras()
            elif opcao == '8':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")