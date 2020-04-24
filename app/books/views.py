from rest_framework import viewsets , mixins

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated 

from core.models import Tag ,Ingredients

from books import serializers

class BaseClass(viewsets.GenericViewSet , mixins.ListModelMixin , mixins.CreateModelMixin) : 
    authentication_classes = (TokenAuthentication ,) 
    permission_classes = (IsAuthenticated,)
    def get_queryset(self) : 
        return self.queryset.filter(user =self.request.user).order_by('-name')
    def perform_create(self , serializer) :
        serializer.save(user =self.request.user) 

class TagViewSet(BaseClass) : 
  
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
 


class IngredientsViewSet(BaseClass ) : 

    queryset = Ingredients.objects.all()
    serializer_class = serializers.IngredientSerializer
