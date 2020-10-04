import graphene
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User
from .userid_gen import uid,otp

class UserType(DjangoObjectType):
    class Meta:
        model=User
        filter_fields = ['mobile']
        interfaces = (relay.Node, )

class UserInput(graphene.InputObjectType):
    name=graphene.String()
    mobile=graphene.String()
    status=graphene.String()
    otp=graphene.String()
    otp_exp_time=graphene.DateTime()
    #price=graphene.Int()
class AddUser(graphene.Mutation):
    class Arguments:
        #id=graphene.ID(required=True)
        input=UserInput(required=True)   
    user=graphene.Field(UserType)

    @staticmethod
    def mutate(root, info,input=None):
        print(input.mobile)
        try:
            user = User.objects.get(mobile=input.mobile)
        #user=info.context.user
            print("user:",user)
            if user.mobile == input.mobile:
                user.name=input.name
        except:
            user = User(
                #name=input.name, 
                mobile=input.mobile, 
                status=input.status,
                #price=input.price,
                )
        user.save()
        return AddUser(user=user)
class ResendOTP(graphene.Mutation):
    class Arguments:
        input=UserInput(required=True)   
    user=graphene.Field(UserType)
    @staticmethod
    def mutate(root, info,input=None):
        try:
            user = User.objects.get(mobile=input.mobile)
        #user=info.context.user
            print("user:",user)
            if user.mobile == input.mobile:
                user.otp=otp.get_otp()
                user.otp_exp_time=otp.get_exp_time()
        except:
            pass
        user.save()
        return ResendOTP(user=user)
class Mutation(ObjectType):
    add_user = AddUser.Field()
    Resend_otp=ResendOTP.Field()

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