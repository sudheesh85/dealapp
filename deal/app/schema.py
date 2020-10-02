from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import User as UserModel
from .crud_hlp import get_object,get_errors,update_create_instance
import graphene

class UserModel(DjangoObjectType):
    class Meta:
        model = UserModel
        filter_fields = ['id','mobile']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    #userinfo = relay.Node.Field(UserModel)
    all_userinfo = DjangoFilterConnectionField(UserModel)
    #user_dtl=relay.Node.Field(UserModel,mobile=graphene.String())


    '''def resolve_user_dtl(self, info,**kwargs):
        ph=kwargs.get("mobile")
        if ph is not None:
            return UserModel.objects.get(mobile=ph)'''
    def resolve_userinfo(self, info):
        #for arg in args:
            return UserModel.objects.all()
#Mutation

class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        filter_fields = ['mobile']
        interfaces = (relay.Node, )
class CreateUser(relay.ClientIDMutation):
  
    class Input:
        # BookCreateInput class used as argument here.
        user = graphene.Argument(UserModel)

    new_user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        mobile = args.get('mobile') # get the book input from the args
        user = UserModel() # get an instance of the book model here
        new_user = update_create_instance(user,mobile) # use custom function to create book

        return cls(new_user=new_user) # newly created book instance returned.


class UpdateUser(relay.ClientIDMutation):

    class Input:
        user = graphene.Argument(UserModel) # get the book input from the args
        id = graphene.String(required=True) # get the book id

    errors = graphene.List(graphene.String)
    updated_user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        try:
            user_instance = get_object(UserModel, args['id']) # get book by id
            if user_instance:
                # modify and update book model instance
                user_data = args.get('mobile')
                updated_user = update_create_instance(user_instance, user_data)
                return cls(updated_book=updated_book)
        except ValidationError as e:
            # return an error if something wrong happens
            return cls(updated_user=None, errors=get_errors(e))
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    #create_book = CreateBook.Field()     
    update_user = UpdateUser.Field() 


schema = graphene.Schema(query=Query,mutation=Mutation)