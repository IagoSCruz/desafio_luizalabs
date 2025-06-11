from django.urls import path
from .views import ProcessadorArquivoView, UserListView, UserDetailView

urlpatterns = [
    # Endpoint POST para enviar o arquivo (via Postman)
    path('processar-arquivo/', ProcessadorArquivoView.as_view(), name='processar_arquivo'),
    
    # Endpoint GET para listar todos os usuários e seus pedidos
    path('users/', UserListView.as_view(), name='user_list'),
    
    # Endpoint GET para buscar um usuário específico: api/user/1/
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
]