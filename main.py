from db_connection import DatabaseConnection
from db_operations import DatabaseOperations
from cli import CLI
1
if __name__ == "__main__":
    # Conexão com o banco
    db_connection = DatabaseConnection()
    produtos_collection = db_connection.get_collection("produtos")
    compras_collection = db_connection.get_collection("compras")

    # Operações do banco
    db_operations = DatabaseOperations(produtos_collection, compras_collection)
    db_operations.inicializar_produtos()

    # Interface de usuário
    cli = CLI(db_operations)
    cli.menu()
