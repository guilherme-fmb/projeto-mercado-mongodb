from datetime import datetime
from bson import ObjectId

class DatabaseOperations:
    def __init__(self, produtos_collection, compras_collection):
        self.produtos_collection = produtos_collection
        self.compras_collection = compras_collection

    def inicializar_produtos(self):
        if self.produtos_collection.count_documents({}) == 0:
            produtos_iniciais = [
                {"codigo": "001", "nome": "Arroz 5kg", "preco": 20.50},
                {"codigo": "002", "nome": "Feijão 1kg", "preco": 8.30},
                {"codigo": "003", "nome": "Macarrão 500g", "preco": 5.75},
                {"codigo": "004", "nome": "Açúcar 2kg", "preco": 7.40},
                {"codigo": "005", "nome": "Óleo de Soja 900ml", "preco": 10.20}
            ]
            self.produtos_collection.insert_many(produtos_iniciais)

    def buscar_produtos(self):
        return list(self.produtos_collection.find())

    def registrar_compra(self, carrinho):
        total = sum(item['preco'] for item in carrinho)
        detalhes_compra = {
            "produtos": [{"nome": item['nome'], "preco": item['preco']} for item in carrinho],
            "total": total,
            "data_hora": datetime.now()
        }
        self.compras_collection.insert_one(detalhes_compra)
        return detalhes_compra

    def buscar_compras_por_data(self, data):
        inicio = datetime(data.year, data.month, data.day, 0, 0, 0)
        fim = datetime(data.year, data.month, data.day, 23, 59, 59)
        return list(self.compras_collection.find({"data_hora": {"$gte": inicio, "$lte": fim}}))

    def buscar_compra_por_id(self, compra_id):
        try:
            return self.compras_collection.find_one({"_id": ObjectId(compra_id)})
        except Exception:
            return None

    def deletar_compra_por_id(self, compra_id):
        try:
            resultado = self.compras_collection.delete_one({"_id": ObjectId(compra_id)})
            return resultado.deleted_count > 0
        except Exception:
            return False

    def adicionar_produto(self, codigo, nome, preco):
        if self.produtos_collection.find_one({"codigo": codigo}):
            return False  # Produto com o mesmo código já existe
        self.produtos_collection.insert_one({"codigo": codigo, "nome": nome, "preco": preco})
        return True

    def exibir_todas_compras(self):
        return list(self.compras_collection.find())