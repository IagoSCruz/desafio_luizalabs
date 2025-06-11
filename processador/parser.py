from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import User, Order, Product

def parse_e_salvar_dados(conteudo_arquivo):
    """
    Analisa as linhas do arquivo e salva os dados no banco de dados.
    Usa uma transação para garantir que o arquivo seja processado por completo ou nada seja salvo.
    """
    linhas = conteudo_arquivo.strip().split('\n')
    

    users_a_criar = {}
    orders_a_criar = {}
    products_a_criar = []

    for linha in linhas:
        if len(linha) < 95: continue
        try:
            user_id = int(linha[0:10])
            name = linha[10:55].strip()
            order_id = int(linha[55:65])
            product_id = int(linha[65:75])
            value = Decimal(linha[75:87])
            date_str = linha[87:95]
            purchase_date = datetime.strptime(date_str, '%Y%m%d').date()

            if not name: continue

            # Agrupa usuários e pedidos para evitar acessos repetidos ao DB dentro do loop
            if user_id not in users_a_criar:
                users_a_criar[user_id] = User(user_id=user_id, name=name)
            
            order_key = (user_id, order_id)
            if order_key not in orders_a_criar:
                orders_a_criar[order_key] = {
                    "user_id": user_id,
                    "order_id": order_id,
                    "purchase_date": purchase_date,
                    "total": Decimal('0.00'),
                    "products": []
                }
            
            orders_a_criar[order_key]["total"] += value
            orders_a_criar[order_key]["products"].append({
                "product_id": product_id,
                "value": value
            })

        except (ValueError, InvalidOperation):
            continue

    # Agora, salva tudo no banco de dados de forma eficiente
    with transaction.atomic():
        # Cria ou atualiza usuários
        for user in users_a_criar.values():
            User.objects.update_or_create(user_id=user.user_id, defaults={'name': user.name})

        # Cria ou atualiza pedidos e seus produtos
        for order_data in orders_a_criar.values():
            order_obj, _ = Order.objects.update_or_create(
                user_id=order_data['user_id'],
                order_id=order_data['order_id'],
                defaults={
                    'purchase_date': order_data['purchase_date'],
                    'total_value': order_data['total']
                }
            )

            # Cria os produtos para este pedido
            produtos_para_o_pedido = []
            for prod in order_data['products']:
                produtos_para_o_pedido.append(
                    Product(order=order_obj, product_id=prod['product_id'], value=prod['value'])
                )
            Product.objects.bulk_create(produtos_para_o_pedido)

    return {"status": "Arquivo processado e dados salvos com sucesso."}