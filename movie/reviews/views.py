from django.shortcuts import render
from .models import Movie, Review, Sentence, Tag
from django.http import JsonResponse, Http404
from django.core import serializers
import json
from collections import defaultdict

# Create your views here.
def index(request):
    return render(request, 'index.html')


def label_info(request):
    data = []   
    if request.method  == "GET":

        movie_id = request.GET['movie_id']
        label_id = request.GET['label_id']

        cluster_id = Tag.objects.get(id = label_id).cluster_id

        movie = Movie.objects.get(movie_id=movie_id)
        reviews = movie.reviews.all()
        sentences = []
        for review in reviews:
            sentences.extend(review.sentences.filter(cluster_id = cluster_id))

        # sentences = Sentence.objects.filter(label = label_id)
        rid_to_sentence = {} 
        rid_to_sim =  defaultdict(int)
        for sent in sentences:
            s_rid = sent.review_id_id
            
            jac_sim = sent.jac_sim
            if jac_sim is None:
                jac_sim=0

            if rid_to_sim[s_rid] <= jac_sim:
                rid_to_sim[s_rid] = jac_sim
                rid_to_sentence[s_rid] = sent #每個review highlight一句就好..

        sort_by_sim = sorted(rid_to_sim.items(), key=lambda x: x[1], reverse=True)
        rid_sorted = [kv[0] for kv in sort_by_sim]

        for rid in rid_sorted:
            element = {}
            rcontent = Review.objects.get(id=rid).content
            element['review'] = rcontent
            element['highlight_sent'] = rid_to_sentence[rid].content
            element['highlight_pos'] = rid_to_sentence[rid].review_position
            data.append(element)
      
    return JsonResponse(json.dumps(data, ensure_ascii=False),safe=False)

def movie_info(request, pk):
    data = {}
    try:
        movie = Movie.objects.get(movie_id=pk)
        data['movie_id'] = pk
        data['title'] = movie.title
        data['title_original'] = movie.title_original
        data['director'] = movie.director
        data['cast'] = movie.cast
        data['image'] = movie.image
        data['length'] = movie.length
        data['date'] = str(movie.date)
        tag_ids = [t.id for t in movie.tags.all()]
        tag_names = [t.name for t in movie.tags.all()]
        data['labels'] = list(zip(tag_ids, tag_names))

    except Movie.DoesNotExist:
        raise Http404
    # return JsonResponse(json.dumps(data, ensure_ascii=False),safe=False)
    return render(request, 'movie_info.html', {'movie': data})

def movie_ls(request):
    # movies = Movie.objects.filter(review_count>150)
    movies =Movie.objects.filter(review_count__gte=150).values('title', 'image','movie_id')

    data = list(movies)
    # for m in movies:
    #     data.append({'title':m['title'] ,'img':m['image'],'id':m['movie_id']})
    data.reverse()
    # return JsonResponse(json.dumps(data, ensure_ascii=False),safe=False)
    return render(request, 'movie_ls.html', {'movies': data})
