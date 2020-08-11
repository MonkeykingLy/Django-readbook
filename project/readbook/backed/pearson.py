from math import sqrt
from .serializers import *
from backed.models import *
import json
from django_redis import get_redis_connection
con=get_redis_connection("default")

# pearson similarity
# 
def pearson_correlation(target, others):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_xx = 0
    sum_yy = 0
    n = 0
    for key in target:
        if key in others:
            n += 1
            x = target[key]
            y = others[key]
            sum_x += x
            sum_y += y
            sum_xy += x * y
            sum_xx += pow(x, 2)
            sum_yy += pow(y, 2)
    if n == 0:
        return 0
    
    denominator = sqrt(sum_xx - pow(sum_x, 2) / n)  * sqrt(sum_yy - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        numerator = sum_xy - (sum_x * sum_y) / n
        return numerator / denominator
# calculate neightbour similarity
def neighbor_similarity(target,datas):
    distance_list=[]
    for key in datas:
        if(key!=target):
            dis=pearson_correlation(datas[target],datas[key])
            distance_list.append((key,dis))
    
    distance_list.sort(key=lambda i:i[1],reverse=True)
    return distance_list

def calculate_correlation(target,datas):
    recommend={}
    distance_list=neighbor_similarity(target,datas)
    total_cor=0
    target_book_list=datas[target]

    for i in distance_list:
        total_cor+=i[1]
    if total_cor==0:
        total_cor=1
    
    for i in range(len(distance_list)):
        weight=distance_list[i][1] / total_cor
        neighbor_id = distance_list[i][0]

        neighbor_books = datas[neighbor_id]
        for j in neighbor_books:
            if j not in target_book_list:
                if j not in recommend:
                    recommend[j]=neighbor_books[j] * weight
                else:
                    recommend[j]+=neighbor_books[j] * weight
    
    rec_list=list(recommend.items())
    rec_list.sort(key=lambda i:i[1],reverse=True)
    # get element which mark >= 0.
    res_list=[]
    for i in rec_list:
        if(i[1]>0):
            res_list.append(i)
    # return top 10.
    if(len(res_list)<5):
        for i in range(5):
            if(rec_list[i] not in res_list):
                res_list.append(rec_list[i])
    return res_list[:10]

def user_recommend(user_id):
    temp_set = Rating.objects.filter(user=str(user_id))
    if(temp_set.count()<=3):
        print("not enough!")
        return 0
    else:
        print('custome recommend')
        data=Rating.objects.all()
        serializer = RecUserBookSerializer(instance=data,many=True)
        user={}
        for i in serializer.data:
            if(i['user'] not in user):
                user[i['user']]={}
            user[i['user']][i['book']]=float(i['rating'])
        res=calculate_correlation(user_id,user)
        con.delete('rec_'+str(user_id))
        for i in res:
            book_temp=Book.objects.get(id=i[0])
            serializer=BookSerializer(instance=book_temp)
            con.rpush('rec_'+str(user_id),json.dumps(serializer.data))
        return 1