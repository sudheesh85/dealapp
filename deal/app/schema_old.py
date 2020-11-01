import graphene
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User

class UserType(DjangoObjectType):
    class Meta:
        model=User
        filter_fields = ['mobile']
        interfaces = (relay.Node, )

class UserInput(graphene.InputObjectType):
    name=graphene.String()
    mobile=graphene.String()
    status=graphene.String()
    #price=graphene.Int()
class AddUser(graphene.Mutation):
    class Arguments:
        input=UserInput(required=True)   
    user=graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        user = User(
            #name=input.name, 
            mobile=input.mobile, 
            status=input.status,
            #price=input.price,
            )
        user.save()
        return AddUser(user=user)

class Mutation(ObjectType):
    add_user = AddUser.Field()

class Query(ObjectType):
    user = graphene.Field(UserType, pk=graphene.Int())
    jeep=graphene.String()
    #all_cars=graphene.List(CarType)
    all_user=DjangoFilterConnectionField(UserType)

    #def resolve_car(self,info):
        #return Car.objects.all()

    def resolve_user(self, info,**kwargs):
        id=kwargs.get("pk")
        if id is not None:
            return User.objects.get(id=id)
        #return f"Mercedes Benz | Model:23qwer | Color: Black"'''
    def resolve_jeep(self,info):
        return f'ya hoo!!!'
    def resolve_all_user(self,info,**kwargs):
        return User.objects.all()

schema = Schema(query=Query,mutation=Mutation)