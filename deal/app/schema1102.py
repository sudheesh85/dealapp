import graphene
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User,Interest,Device,Yesdeal,Branch
from .userid_gen import uid,otp
from datetime import datetime as dt

class YesdealType(DjangoObjectType):
    class Meta:
        model = Yesdeal
        filter_fields=[]
        interfaces = (relay.Node,)

class UserType(DjangoObjectType):
    class Meta:
        model=User
        filter_fields = ['mobile']
        interfaces = (relay.Node, )
class InterestType(DjangoObjectType):
    class Meta:
        model = Interest
        filter_fields=[]
        interfaces = (relay.Node, )
class DeviceType(DjangoObjectType):
    class Meta:
        model=Device
        filter_fields=[]
        interfaces=(relay.Node,)
class YesdealInput(graphene.InputObjectType):
    pass

class UserInput(graphene.InputObjectType):
    name=graphene.String(required=False)
    userCD=graphene.String()
    mobile=graphene.String(required=True)
    status=graphene.String()
    interest=graphene.List(graphene.String)
    otp=graphene.String()
    otp_exp_time=graphene.DateTime()
    is_otp_verified=graphene.Boolean()
    
class DeviceInput(graphene.InputObjectType):
    device=graphene.JSONString()

class addDevice(graphene.Mutation):
    class Arguments:
        #userCD=graphene.String()
        input=UserInput(required=True) 
        device=DeviceInput()
    device=graphene.Field(DeviceType)
    @staticmethod
    def mutate(root,info,input=None,device=None):
        print(device.device)
        user=User.objects.get(mobile=input.mobile)
        print(user.userCD)
        device=Device.objects.create(userCD=user,device=device.device)
        device.save()
        return addDevice(device=device)

class AddUser(graphene.Mutation):
    class Arguments:
        #id=graphene.ID(required=True)
        input=UserInput(required=True) 
    ok=graphene.String()  
    user=graphene.Field(UserType)

    @staticmethod
    def mutate(root, info,input=None):
        print(input.mobile)
        user,created = User.objects.get_or_create(mobile=input.mobile)
        print("user:",created)
        if created:
            user.save()
            ok="New user hs been created"
            return AddUser(user=user,ok=ok)
        if user.mobile == input.mobile:
            if input.name:
                user.name=input.name
            if input.interest:
                #user.interest=input.interest
                user.interest.set(input.interest)
        user.save()
        ok="User has been updated"
        return AddUser(user=user,ok=ok)

class verifyOTP(graphene.Mutation):
    class Arguments:
        input=UserInput(required=True)
    ok = graphene.Boolean()
    user=graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,input=None):
        try:
            user=User.objects.get(userCD=input.userCD)
            ctime=dt.now()
            condition=[user.otp==input.otp,not user.is_otp_verified,ctime < otp_exp_time]
            if all(condition):
                user.is_otp_verified=True
                ok=True
            else:
                ok=False
        except:
            ok=False
        user.save()
        return verifyOTP(user=user,ok=ok)

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
class InterestInput(graphene.InputObjectType):
    category_name=graphene.String()
    category_id = graphene.Int()
class AddInterest(graphene.Mutation):
    class Arguments:
        input=InterestInput(required=True)
    interest=graphene.Field(InterestType)
    @staticmethod
    def mutate(root,info,input=None):

        interest=Interest(
            category_id=input.category_id,
            category_name=input.category_name
        )
        interest.save()
        return AddInterest(interest=interest)
class Mutation(ObjectType):
    add_user = AddUser.Field()
    Resend_otp=ResendOTP.Field()
    verify_otp=verifyOTP.Field()
    add_interest=AddInterest.Field()
    add_device=addDevice.Field()

class Query(ObjectType):
    user = graphene.Field(UserType, pk=graphene.Int())
    interest=graphene.Field(InterestType,pk=graphene.Int())
    deal = graphene.List(lambda:graphene.List(YesdealType),pk=graphene.String())
    jeep=graphene.String()
    #all_cars=graphene.List(CarType)
    all_user=DjangoFilterConnectionField(UserType)
    all_interest=DjangoFilterConnectionField(InterestType)
    all_device=DjangoFilterConnectionField(DeviceType)
    all_deal = DjangoFilterConnectionField(YesdealType)

    #def resolve_car(self,info):
        #return Car.objects.all()

    def resolve_user(self, info,**kwargs):
        id=kwargs.get("pk")
        if id is not None:
            return User.objects.get(id=id)
        #return f"Mercedes Benz | Model:23qwer | Color: Black"'''
    def resolve_deal(self,info,**kwargs):
        userCD = kwargs.get("pk")
        if userCD is not None:
            user = User.objects.get(userCD=userCD)
            #a=app_user_interest.objects.all()
            #print(a)
            #intr=a.category_name.all(user_id=user.id)
            #print(user.id)
            user_deal=[]
            interest=user.interest.all().values('id')

            print(interest)
            for value in interest:
                for key,id in value.items():
                    #print(id)
                    coll_deal = Yesdeal.objects.filter(deal_category_id=id)
                    print(id,coll_deal)
                    if coll_deal:
                        user_deal.append(coll_deal)
            return user_deal
    def resolve_all_deal(self,info,**kwargs):
        return Yesdeal.objects.all()
    def resolve_jeep(self,info):
        return f'ya hoo!!!'
    def resolve_all_user(self,info,**kwargs):
        return User.objects.all()
    def resolve_interest(self,info,**kwargs):
        id=kwargs.get("pk")
        if id is not None:
            return Interest.objects.get(id=id)
    def resolve_all_interest(self,info,**kwargs):
        return Interest.objects.all()
    def resolve_all_device(self,info,**kwargs):
        return Device.objects.all()

schema = Schema(query=Query,mutation=Mutation)