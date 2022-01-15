from rest_framework.views import APIView
from .forms import NewUserForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    http_method_names = ['post']
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        form = NewUserForm(data=request.POST)
        
        if form.is_valid():
            user = form.save()
            tok = RefreshToken.for_user(user)
            return Response({
                'status': True,
                'tokens': {
                    'refresh': str(tok),
                    'access': str(tok.access_token)
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': False,
            'errors': form.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)