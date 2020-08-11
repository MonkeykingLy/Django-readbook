from django.shortcuts import render
from account.models import *
from django.contrib.auth.hashers import make_password,check_password
import django.dispatch
from django.dispatch import receiver
from django.utils import timezone

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

#
from .serializers import *
from backed.pearson import *
from backed.simple_rec import *

# redis
# import json
from django_redis import get_redis_connection
con=get_redis_connection("default")

# when server run, clean the redis.
con.flushdb()

# run simple recommendation and put them into redis.
operation()

##### signals
# goal_add=django.dispatch.Signal(providing_args=['user_id','year','month'])
# goal_del = django.dispatch.Signal(providing_args=['user_id','year','month'])


######################## main #######################

# get token, return token,username and user id
class CustomAuthToken(ObtainAuthToken):
    #
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            ob=serializer.validated_data
            user = serializer.validated_data['user']
            # trigger recommend
            temp=user_recommend(int(user.id))
            print(temp)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username,'user_id':user.id},status=HTTP_200_OK)
        print(serializer.errors)
        username = request.data['username']
        # username is unique, so just check username
        counts = Account.objects.filter(username=username).count()
        if counts:
            return Response(data={'msg':"Please Check Your Password!"} ,status=HTTP_400_BAD_REQUEST,content_type='application/json')
        return Response(data={'msg':"User doesn't exist!"} ,status=HTTP_400_BAD_REQUEST,content_type='application/json')

# register new user, return token , username, user id.
class RegisterAPIView(APIView):
    
    # 
    def post(self, request, format=None):
        print(request.data)
        res = RegSerializer(data = request.data, context={'request': request})
        username = request.data['username']
        if res.is_valid():
            res.save()
            user = Account.objects.get(username=username)
            collection_temp={}
            collection_temp["name"]=user.username+"'s collection"
            collection_temp["user"]=user.id
            default_collection = CollectionSerializer(data=collection_temp)
            if(default_collection.is_valid()):
                default_collection.save()
                temp=user_recommend(int(user.id))
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username,'user_id':user.id},status=HTTP_200_OK)
        print(res.errors)
        return Response(data={'msg':"Username is exist!"} ,status=HTTP_400_BAD_REQUEST,content_type='application/json')

# get account detail, username, email, birth-day
# collections: collection name,id,books
# books detail
class AccountDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        print(token)
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        print(type(user_obj))
        serializer = AccountDetailSerializer(instance=user_obj)
        account_data=serializer.data
        account_data['join_date']=account_data['join_date'][:10]
        return Response(data=account_data, status=HTTP_200_OK)
    
    def post(self,request,format=None):
        user_id=request.data['id']
        user_obj=Account.objects.get(id=user_id)
        user_obj.date_of_birth=request.data['date_of_birth']
        user_obj.gender = request.data['gender']
        user_obj.save()
        return Response(data={"msg":"edit success!"},status=HTTP_200_OK)

# collection operation, get,delete,create,rename
class CreateCollectionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # get exactly collection, return detail
    def get(self,request, format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        print(user_obj)
        collect_set = Collection.objects.filter(user=user_obj.id)
        if(collect_set.exists()):
            serializer = CollectionSerializer(instance=collect_set, many=True)
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response(data={"msg":"No Colletions!"},status=HTTP_400_BAD_REQUEST)
        

    # 
    # create new collection
    def post(self, request, format=None):
        print(request.data)
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        temp=request.data
        temp['user']=user_obj.id
        collect = CollectionSerializer(data=temp)
        if collect.is_valid():
            collect.save()
            return Response(data={"msg":'collection create success!'},status=HTTP_200_OK)
        print(collect.errors)
        return Response(status=HTTP_400_BAD_REQUEST)

    
    # delete collection
    def delete(self, request, format=None):
        print('delete')
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        print(request.data)
        collection_id = request.data["collection_id"]
        Collection.objects.filter(id=collection_id,user=user_obj.id).delete()
        return Response(data={'msg':'already delete!'},status=HTTP_200_OK)
    
    # collection rename
    def put(self,request,format=None):
        print(request.data)
        collect_id = request.data['collection_id']
        new_name = request.data['new_name']
        collection_set = Collection.objects.filter(id=collect_id)
        if(collection_set.exists()):
            collection_temp=collection_set[0]
            collection_temp.name=new_name
            collection_temp.save()
            return Response(data={"msg":'name change success'},status=HTTP_200_OK)
        else:
            return Response(data={"msg":"no collection id!"},status=HTTP_400_BAD_REQUEST)

        
# add book into database
class AddBookAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        book_info = request.data['book_info']
        book_set=Book.objects.filter(id=book_info["id"])
        if(book_set.exists()):
            return Response(data={"msg":"already in database!"},status=HTTP_200_OK)
        else:
            serializer = BookSerializer(data=book_info)
            if(serializer.is_valid()):
                serializer.save()
                return Response(data={"msg":"add it success"},status=HTTP_200_OK)
            print(serializer.errors)
            return Response(data={"mag":"error"},status=HTTP_400_BAD_REQUEST)

# filter search
class FilterSearchBookAPIView(APIView):
    def get(self,request,format=None):
        info=request.query_params
        print('filter')
        search_key=info['key_word']
        search_type=info['search_type']
        filter_rating = int(info['filter_rating'])
        if search_type.lower() == "title":
            print('yes')
            search_set = Book.objects.filter(title__contains = search_key,avg_rating__gte=filter_rating).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        elif search_type.lower() == 'authors':
            search_set = Book.objects.filter(authors__contains = search_key,avg_rating__gte=filter_rating).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                # res=[]
                # for i in serializer.data:
                #     if(i['avg_rating']>=filter_rating):
                #         res.append(i)
                # res.sort(key=lambda i:i['avg_rating'],reverse=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"msg":"search type error!"},status=HTTP_400_BAD_REQUEST)


# search book by title,author, account
class SearchBookAPIView(APIView):
    def post(self, request, format=None):
        print(request.data)
        print('search not filter')
        search_type = request.data['search_type']
        if search_type.lower() == "title":
            search_key = request.data['key_word']
            search_set = Book.objects.filter(title__contains = search_key).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        elif search_type.lower() == 'authors':
            search_key = request.data['key_word']
            search_set = Book.objects.filter(authors__contains = search_key).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"msg":"search type error!"},status=HTTP_400_BAD_REQUEST)
        
    def get(self,request,format=None):
        data=request.query_params
        search_key=data['key_word']
        search_type=data['search_type']
        if search_type.lower() == "title":
            search_set = Book.objects.filter(title__contains = search_key).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        elif search_type.lower() == 'authors':
            search_set = Book.objects.filter(authors__contains = search_key).order_by('-avg_rating')
            if search_set.exists():
                serializer = BookSerializer(instance=search_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST) 
        elif search_type.lower() == 'user':
            users_set = Account.objects.filter(username__contains = search_key)
            if(users_set.exists()):
                serializer=OtherAccountDetailSerializer(instance=users_set,many=True)
                return Response(serializer.data,status=HTTP_200_OK)
            else:
                return Response(data={"msg":"no result!"},status=HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"msg":"search type error!"},status=HTTP_400_BAD_REQUEST)


# add book into collection
class AddBookToCollectionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # 
    def post(self,request,format=None):
        print(request.data)
        time_now=timezone.now()
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        book_id = request.data["book_id"]
        collection_id = request.data["collection_id"]
        relation_check_set = Collection_Book.objects.filter(collection=collection_id,book=book_id)
        if(relation_check_set.exists()):
            return Response(data={"msg":" this book already in this collection!"},status=HTTP_400_BAD_REQUEST)
        book_obj = Book.objects.get(id=book_id)
        collection_obj = Collection.objects.get(id=collection_id)
        book_collection_relation = Collection_Book(collection=collection_obj,book=book_obj,belongto=user_obj.id)
        book_collection_relation.save()
        book_obj.added_times+=1
        book_obj.save()
        readed_set=ReadedBook.objects.filter(user=user_obj.id,book_id=book_id)
        if(readed_set.exists()==False):
            print('readed add')
            temp={}
            temp['user']=user_obj.id
            temp['book_id']=book_id
            read_ser=ReadedBookSerializer(data=temp)
            if read_ser.is_valid():
                read_ser.save()
        # goal_add.send(AddBookToCollectionAPIView,user_id=user_obj.id,year=time_now.year,month=time_now.month)
        return Response(data={"msg":"add it success!"},status=HTTP_200_OK)
    
    # remove book from collection 
    def delete(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        time_now=timezone.now()
        book_id = request.data["book_id"]
        collection_id = request.data["collection_id"]
        Collection_Book.objects.filter(collection=collection_id,book=book_id,belongto=user_obj.id).delete()
        # goal_del.send(AddBookToCollectionAPIView,user_id=user_obj.id,year=time_now.year,month=time_now.month)
        return Response(data={"msg":"delete it success"},status=HTTP_200_OK)


# rating
class ReviewAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # create new review and update review
    def post(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        book_id = request.data['book_id']
        review_info = request.data['review']
        # it will check content length, avoid empty review.
        if(len(review_info['content'])<=5):
            return Response(data={"msg":"review is too short"},status=HTTP_400_BAD_REQUEST)
        else:
            try:
                # try acquire review_id, if get ,it means update review
                review_id=request.data["review_id"]
                review_temp=Review.objects.get(id=review_id)
                review_temp.content=review_info['content']
                review_temp.save()
                return Response(data={"msg":"update success!"},status=HTTP_200_OK)
            except:
                # if not get review id, create new review
                # new review will return review objects, include review id
                review_info['user']=user_obj.id
                review_info['book']=book_id
                serializer = ReviewSerializer(data=review_info)
                if serializer.is_valid():
                    serializer.save()
                    print('ready to save')
                    return Response(data={'msg':serializer.data},status=HTTP_200_OK)
                print(serializer.errors)
                return Response(data={'msg':'error'},status=HTTP_400_BAD_REQUEST)


# mark some book
class RatingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        rating_info = request.data['rating_info']
        rating_set=Rating.objects.filter(user=user_obj.id,book=rating_info['book'])
        if(rating_set.exists()):
            # check data, if exists, update rating
            rating_temp=rating_set[0]
            rating_temp.rating = rating_info['rating']
            rating_temp.save()
            book_id=rating_info['book']
            rating_count_set = Rating.objects.filter(book=book_id)
            temp=0
            for i in rating_count_set:
                temp+=i.rating
            avg_temp=round(temp/rating_count_set.count(),1)
            book_temp=Book.objects.get(id=book_id)
            book_temp.avg_rating=avg_temp
            book_temp.save()
            return Response(data={"msg":'update success!'},status=HTTP_200_OK)

        else:
            # doesn't exists, create new rating relation
            rating_info['user']=user_obj.id
            serializer = RatingSerializer(data=rating_info)
            if serializer.is_valid():
                serializer.save()
                book_id=rating_info['book']
                rating_count_set = Rating.objects.filter(book=book_id)
                temp=0
                for i in rating_count_set:
                    temp+=i.rating
                avg_temp=round(temp/rating_count_set.count(),1)
                book_temp=Book.objects.get(id=book_id)
                book_temp.avg_rating=avg_temp
                book_temp.save()
                return Response(data={'msg':'add rating success'},status=HTTP_200_OK)
            print(serializer.errors)
            return Response(data={'msg':'error'},status=HTTP_400_BAD_REQUEST)

# like function
class LikeItAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # create like function
    def post(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        review_id = request.data['review_id']
        like_info = request.data['likeit']

        like_set=LikeIt.objects.filter(review=review_id,user=user_obj.id)
        if(like_set.exists()):
            if(like_info["status"]==-1):
                # if status = -1, it means doesn't like!
                like_new_info = like_set[0]
                if(like_new_info.status==0):
                    return Response(data={"msg":"op!"},status=HTTP_400_BAD_REQUEST)
                like_new_info.status=0
                like_new_info.save()
                review_new_temp=Review.objects.get(id = review_id)
                review_new_temp.like_count_num-=1
                review_new_temp.save()
                return Response(data={'msg':'wow!'},status=HTTP_200_OK)
            else:
                # if like some review before, then un-like
                like_new_info = like_set[0]
                if(like_new_info.status==1):
                    return Response(data={"msg":"别折腾了"},status=HTTP_400_BAD_REQUEST)
                like_new_info.status=1
                like_new_info.save()
                review_new_temp=Review.objects.get(id = review_id)
                review_new_temp.like_count_num+=1
                review_new_temp.save()
                return Response(data={"msg":"我又点赞了！"},status=HTTP_200_OK)
            return Response(data={"msg":"already like it!"},status=HTTP_200_OK)
        else:
            # create new like relation in database.
            likeit_info = request.data['likeit']
            likeit_info['user']=user_obj.id
            likeit_info['review']=review_id
            likeit_info['belongto_book']=request.data['book_id']
            serializer = LikeItSerializer(data=likeit_info)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['status']==1:
                    print("likeit")
                    review_temp=Review.objects.get(id=review_id)
                    review_temp.like_count_num+=1
                    review_temp.save()
                return Response(data={'msg':'like it!'},status=HTTP_200_OK)
            print(serializer.errors)
            return Response(data={'msg':'error'},status=HTTP_400_BAD_REQUEST)
    
# click one book request data is book_id
# check book infomation
# if will check header token:
# if header has token and token is valid:
# the return data will include user's action 
# else:
# return data with out user action
# 
# rating nanlyse: include all rating about this book
# reviews: include all review related to this book.
# 
class BookDetailPageAPIView(APIView):

    def get(self,request,format=None):
        data=request.query_params
        book_id = data['book_id']
        book_set = Book.objects.filter(id=book_id)
        book_obj = book_set[0]

        if(book_set.exists()):
            try:
                token=request.META.get('HTTP_AUTHORIZATION')
                token=token.split()
                token_obj=Token.objects.get(key=token[1])
                user_obj = token_obj.user
            except:
                serializer = BookDetailPageNoUserSerializer(instance=book_obj)
                return Response(serializer.data,status=HTTP_200_OK)
            serializer = BookDetailPageSerializer(instance=book_obj,context={'user_id': user_obj.id})
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response(data={"msg":"No Book!"},status=HTTP_400_BAD_REQUEST)


#  set monthly goal
class MonthlyGoalAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    # get goal info, if user never set any goal, it will return 0,0.
    def get(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        data=request.query_params
        month_data= data['month']
        year_data=data['year']
        print(request.data)
        goal_set = Goal.objects.filter(user=user_obj.id,year=year_data,month=month_data)
        if(goal_set.exists()):
            goal_data=goal_set[0]
            ans = Collection_Book.objects.filter(belongto=user_obj.id,create_time__year=year_data,create_time__month=month_data)
            num=0
            if(ans.exists()):
                num=ans.count()
            return Response(data={"target":goal_data.target,"already_done":num},status=HTTP_200_OK)
        else:
            return Response(data={"target":0,"already_done":0},status=HTTP_200_OK)   

    # create goal relation
    # it will check data and return how many book add into collection in this month.
    def post(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        goal_info = request.data['month_goal']
        goal_info['user']=user_obj.id
        goal_set = Goal.objects.filter(user=user_obj.id,year=goal_info['year'],month=goal_info['month'])
        if(goal_set.exists()):
            goal_temp = goal_set[0]
            goal_temp.target = goal_info['target']
            goal_temp.save()
            ans = Collection_Book.objects.filter(belongto=user_obj.id,create_time__year=goal_info['year'],create_time__month=goal_info['month'])
            num=0
            if(ans.exists()):
                num=ans.count()
            return Response(data={"msg":"edit set success","already_done":num},status=HTTP_200_OK)
        else:
            serializer = MonthlyGoalBaseSerializer(data=goal_info)
            if(serializer.is_valid()):
                serializer.save()
                # res = MonthlyGoalAPIView(isinstance=goal_info)
                ans = Collection_Book.objects.filter(belongto=user_obj.id,create_time__year=goal_info['year'],create_time__month=goal_info['month'])
                num=0
                if(ans.exists()):
                    num=ans.count()
                return Response(data={"msg":"set success","already_done":num},status=HTTP_200_OK)
            print(serializer.errors)
            return Response(data={"msg":"errors"},status=HTTP_400_BAD_REQUEST)



######################main page recommend ############# 
# main page recommend api, it will check redis database first.
class MainPageRecAPIView(APIView):

    def get(self,request,format=None):
        if(con.exists('mainpagelist')):
            temp=con.lrange('mainpagelist',0,-1)
            res=[]
            for i in temp:
                res.append(json.loads(i))
            return Response(data=res,status=HTTP_200_OK)
        else:
            main_page_rec_set = Book.objects.all().order_by('-avg_rating','-added_times')[:5]
            serializer = BookSerializer(instance=main_page_rec_set,many=True)
            return Response(serializer.data)

# recommend api
# if user's book satisfy the conditions, it will generate custom recommend
# else, just recommend high rating 
class UserBaseRecAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        token=request.META.get('HTTP_AUTHORIZATION')
        token=token.split()
        token_obj=Token.objects.get(key=token[1])
        user_obj = token_obj.user
        user_id=user_obj.id
        if(con.exists('rec_'+str(user_id))):
            print('get from cache')
            temp=con.lrange('rec_'+str(user_id),0,-1)
            rec=[]
            for i in temp:
                rec.append(json.loads(i))
            res_rating=[]
            res_add=[]
            temp_1=con.lrange('highrating',0,-1)
            for i in temp_1:
                res_rating.append(json.loads(i))
            temp_2=con.lrange('highadded',0,-1)
            for i in temp_2:
                res_add.append(json.loads(i))
            return Response(data={"rec":rec,"rating_rec":res_rating,"added_rec":res_add},status=HTTP_200_OK)
        else:
            res_rating=[]
            res_add=[]
            temp_1=con.lrange('highrating',0,-1)
            for i in temp_1:
                res_rating.append(json.loads(i))
            temp_2=con.lrange('highadded',0,-1)
            for i in temp_2:
                res_add.append(json.loads(i))
            # data={"rating_rec":res_rating,"added_rec":res_add}
            flag=user_recommend(user_id)
            if(flag):
                temp=con.lrange('rec_'+str(user_id),0,-1)
                rec=[]
                for i in temp:
                    rec.append(json.loads(i))
                return Response(data={"rec":rec,"rating_rec":res_rating,"added_rec":res_add},status=HTTP_200_OK)
            else:
                return Response(data={"rating_rec":res_rating,"added_rec":res_add},status=HTTP_200_OK)


# abort……
class HistoryAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        info = request.query_params
        user_id=info['id']
        user_obj=Account.objects.get(id=user_id)
        serializer=HistorySerializer(instance=user_obj)
        return Response(serializer.data)



# test

class TestAPIView(APIView):
    def get(self,request,format=None):
        res=0
        if(con.exists('rec_'+str(3))):
            res=1
        return Response(data=res)



#######
#
# @receiver(goal_add,sender=AddBookToCollectionAPIView)
# def goal_add_callback(sender, **kwargs):
#     rec_set=MonthRecord.objects.filter(user=kwargs['user_id'],year=kwargs['year'],month=kwargs['month'])
#     if(rec_set.exists()):
#         rec_temp=rec_set[0] 
#         rec_temp.total_nums+=1
#         rec_temp.save()
#     else:
#         rec_obj={}
#         rec_obj['user']=kwargs['user_id']
#         rec_obj['year']=kwargs['year']
#         rec_obj['month']=kwargs['month']
#         rec_obj['total_nums']=1
#         serializer = MonthRecordSerializer(data=rec_obj)
#         if(serializer.is_valid()):
#             serializer.save()
#
# @receiver(goal_del,sender=AddBookToCollectionAPIView)
# def goal_del_callback(sender, **kwargs):
#     rec_set=MonthRecord.objects.get(user=kwargs['user_id'],year=kwargs['year'],month=kwargs['month']) 
#     rec_temp=rec_set[0]
#     rec_temp.total_nums-=1
#     rec_temp.save()


        
















  
        

            


