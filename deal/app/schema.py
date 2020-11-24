import graphene
import graphql_jwt
from graphene import relay,ObjectType, Schema,Mutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from app.models import User,Interest,Device,Yesdeal,Branch,Vendor
from .userid_gen import uid,otp
from .passwd_gen import tok
from datetime import datetime as dt
from django.utils import timezone
from graphql import GraphQLError


class YesdealType(DjangoObjectType):
    class Meta:
        model = Yesdeal
        filter_fields=[]
        interfaces = (relay.Node,)
class VendorType(DjangoObjectType):
    class Meta:
        model = Vendor
        filter_fields=[]
        interfaces = (relay.Node,)
class BranchType(DjangoObjectType):
    class Meta:
        model = Branch
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
    deal_sku_cd = graphene.String()
    deal_title = graphene.String()
    deal_desc = graphene.String()
    deal_org_price = graphene.Float()
    deal_spl_price = graphene.Float()
    deal_category = graphene.Int()
    deal_count = graphene.Int()
    deal_vendor = graphene.Int()
    deal_available_branch = graphene.Int()
class VendorInput(graphene.InputObjectType):
    pass
class BranchInput(graphene.InputObjectType):
    pass

class UserInput(graphene.InputObjectType):
    name=graphene.String()
    userCD=graphene.String()
    user_token = graphene.String()
    mobile=graphene.String()
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
        else:
            ok="User already exist please call UpdateUser"
            return AddUser(ok=ok)
class SendOTP(graphene.Mutation):
    class Arguments:
        mobile = graphene.String()
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,mobile):
        user,created = User.objects.get_or_create(mobile=mobile)
        if created:

            ok="OTP for new user has been created"
        else:
            user.user_token = tok.get_token()
            user.otp=otp.get_otp()
            user.is_otp_verified=False
            user.otp_exp_time=otp.get_exp_time()
            ok="OTP for existing user has been created"
        user.save()
        return SendOTP(user=user,ok=ok)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput()
    ok=graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,input=None):
        user = User.objects.get(userCD = input.userCD)
        if user.user_token == input.user_token :
            if user.userCD == input.userCD  :
                if input.name:
                    user.name=input.name
                #if input.mobile:
                    #user.mobile=input.mobile
                if input.interest:
                    #user.interest=input.interest
                    user.interest.set(input.interest)
            user.save()
            ok="User has been updated"
            return UpdateUser(user=user,ok=ok)
        else:
            raise GraphQLError('User must be authenticated')


class verifyOTP(graphene.Mutation):
    class Arguments:
        input=UserInput(required=True) 
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,input=None):
        user=User.objects.get(mobile=input.mobile)
        ctime=timezone.now()
        print(ctime)
        condition=[user.otp==input.otp,not user.is_otp_verified,ctime < user.otp_exp_time]
        if not user.userCD:
            user.userCD = uid.make_id()
            user.created_at = ctime
            if all(condition):
                user.is_otp_verified=True
                user.otp="xxxxxx"
                ok="OTP has been verified and user has been created"
            else:
                ok="OTP verification failed"
        else:
            if all(condition):
                user.is_otp_verified=True
                user.otp="xxxxxx"
                ok="OTP has been verified"
            else:
                user.is_otp_verified=False
                ok="OTP verification failed"
        user.save()
        return verifyOTP(user=user,ok=ok)

class ResendOTP(graphene.Mutation):
    class Arguments:
        mobile = graphene.String()
    ok = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root,info,mobile):
        try:
            user = User.objects.get(mobile=mobile)
            user.user_token = tok.get_token()
            user.otp=otp.get_otp()
            user.is_otp_verified=False
            user.otp_exp_time=otp.get_exp_time()
            ok="OTP for existing user has been resent"
            user.save()
            return ResendOTP(user=user,ok=ok)
        except:
            ok="User does not exist"
            return ResendOTP(ok=ok)
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
class AddDeal(graphene.Mutation):
    class Arguments:
        input = YesdealInput()
    deal = graphene.Field(YesdealType)
    @staticmethod
    def mutate(root,info,input=None):
        vendor_obj = Vendor.objects.get(id=input.deal_vendor)
        category_obj = Interest.objects.get(id=input.deal_category)
        branch_obj = Branch.objects.get(id=input.deal_available_branch)
        #input.deal_vendor = vendor
        deal=Yesdeal.objects.create(
            deal_vendor=vendor_obj,
            deal_title=input.deal_title,
            deal_desc = input.deal_desc,
            deal_count=input.deal_count,
            deal_org_price = input.deal_org_price,
            deal_spl_price = input.deal_spl_price,
            deal_category=category_obj,
            deal_available_branch = branch_obj)
        #if deal:
        deal.save()
        return AddDeal(deal=deal)
class Mutation(ObjectType):
    #add_user = AddUser.Field()
    Resend_otp=ResendOTP.Field()
    verify_otp=verifyOTP.Field()
    add_interest=AddInterest.Field()
    add_device=addDevice.Field()
    update_user=UpdateUser.Field()
    add_deal = AddDeal.Field()
    #token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    #verify_token = graphql_jwt.Verify.Field()
    #refresh_token = graphql_jwt.Refresh.Field()
    sendOTP = SendOTP.Field()

class Query(ObjectType):
    user = graphene.Field(UserType, userCD=graphene.String())
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
        userCD=kwargs.get("userCD")
        user = info.context.user
        print(user)
        if userCD is not None:
            return User.objects.get(userCD=userCD)
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