import json
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from ads.models import Ad, Category
from csv_v_json import csvs_v_jsons, load_data_ads, load_data_cat


def index(request):  # (подход FBV)
    response = {"status": "ok"}
    return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ads_View(View):
    """ для /ad метод GET """

    def get(self, request):
        response = []
        for ad in Ad.objects.all():
            dict_obj = vars(ad)
            dict_obj.pop('_state')
            response.append(dict_obj)

        return JsonResponse(response, safe=False, status=200)

    # """ для /ad метод POST """
    def post(self, request):
        dict_data = json.loads(request.body)
        ad = Ad()
        for key in dict_data:
            setattr(ad, key, dict_data[key])
        ad.save()

        response = vars(ad)
        response.pop('_state')
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ad_View(DetailView):
    model = Ad

    # """ для /ad/:id метод GET """
    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            return JsonResponse({"error": "not found"}, status=404)
        else:
            response = vars(obj)
            response.pop('_state')
            return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Cats_View(View):
    """ для /cat метод GET """

    def get(self, request):
        response = []
        for cat in Category.objects.all():
            dict_obj = vars(cat)
            dict_obj.pop('_state')
            response.append(dict_obj)

        return JsonResponse(response, safe=False, status=200)

    # """ для /cat метод POST """
    def post(self, request):
        dict_data = json.loads(request.body)
        cat = Category()
        for key in dict_data:
            setattr(cat, key, dict_data[key])
        cat.save()

        response = vars(cat)
        response.pop('_state')
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Cat_View(DetailView):
    model = Category

    # """ для /cat/:id метод GET """
    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            return JsonResponse({"error": "not found"}, status=404)
        else:
            response = vars(obj)
            response.pop('_state')
            return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Csv_in_Json(View):
    """ для /csv_v_json метод GET , используя хитрость и смекалку"""

    def get(self, request):
        csvs_v_jsons()
        response = {"csv->json": "ok"}
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Csv_in_Bd(View):
    """ для /csv_v_bd метод GET , загрузка данных из csv в таблицу"""

    def get(self, request):
        if load_data_ads(Ad) and load_data_cat(Category):
            response = {"csv->bd": "ok"}
            return JsonResponse(response, status=200)
        else:
            response = {"csv->bd": "no"}
            return JsonResponse(response, status=400)
