from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .parser import parse_e_salvar_dados
# Create your views here.


class ProcessadorArquivoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

       # VERIFICAR SE O ARQUIVO FOI ENVIADO NA REQUISIÇÃO
        if 'file' not in request.FILES:
            return Response(
                {"erro": "Nenhum arquivo foi enviado. Use a chave 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        arquivo_enviado = request.FILES['file']

        try:
            conteudo_arquivo = arquivo_enviado.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response(
                {"erro": "Verifique se está em UTF-8."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultado = parse_e_salvar_dados(conteudo_arquivo)

        return Response(resultado, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = User.objects.prefetch_related('orders__products').all().order_by('user_id')
    serializer_class = UserSerializer

# View para buscar um usuario específico pelo ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.prefetch_related('orders__products').all()
    serializer_class = UserSerializer
    lookup_field = 'user_id' # Diz a API para buscar pelo nosso campo 'user_id'