from django.db import models

# Create your models here.

# processador/models.py
from django.db import models

class User(models.Model):
    # user_id do arquivo como primary key
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (ID: {self.user_id})"

class Order(models.Model):
    # Chave estrangeira aqui é o ID que o Django gera.
    order_id = models.IntegerField()
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    purchase_date = models.DateField()
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    class Meta:
        # Puxa a combinação de usuário e order_id para ser única.
        unique_together = ('user', 'order_id')

    def __str__(self):
        return f"Pedido {self.order_id} de {self.user.name}"

class Product(models.Model):
    product_id = models.IntegerField()
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Produto {self.product_id} (Valor: {self.value})"