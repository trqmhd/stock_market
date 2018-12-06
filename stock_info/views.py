from django.shortcuts import render, get_object_or_404

from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView
from .models import StockInfo
from django.http import HttpResponse
from django.db.models import Q

from stock_trade.models import Trade


# Create your views here.
class StockListView(ListView):
    #queryset = StockInfo.objects.all()
    template_name = "stock_info/stock_list_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StockListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return StockInfo.objects.all()


def stock_list_view(request):
    queryset = StockInfo.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "stock_info/stock_list_view.html", context)






class StockDetailView(DetailView):
    #queryset = StockInfo.objects.all()
    template_name = "stock_info/stock_detail_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StockDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = StockInfo.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")

        return instance


    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return StockInfo.objects.filter(pk=pk)


def stock_detail_view(request, pk=None, *args, **kwargs):
    # instance = get_object_or_404(StockInfo, pk=pk)
    # try:
    #     instance = StockInfo.objects.get(id=pk)
    # except StockInfo.DoesNotExist:
    #     # print("This stock are not available")
    #     raise Http404("Stock doesn't exist")
    # except:
    #     print("Sorry")
    instance = StockInfo.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    # qs = StockInfo.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }

    return render(request, "stock_info/stock_detail_view.html", context)






# search view:
from stock_info.models import StockInfo


class SearchStockView(ListView):
    template_name = "stock_info/stock_list_view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        print(query)
        if query is not None:
            lookup = Q(symbol__icontains = query) | Q(id__icontains= query)
            return StockInfo.objects.filter(lookup). distinct() # distinct remove redundant product
        return StockInfo.objects.none()


'''
def SearchStockView(request):
    queryset = StockInfo.objects.filter(symbol__icontains ="AAPL") #iexact
    context = {
        'object_list' : queryset
    }
    return render(request, "stock_info/stock_list_view.html", context)

'''



class StockDetailSlugView(DetailView):
    queryset = StockInfo.objects.all()
    template_name = "stock_info/stock_detail_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StockDetailSlugView, self).get_context_data(*args, **kwargs)
        request = self.request
        trade_obj, new_obj = Trade.objects.new_or_get(request)
        context['trade'] = trade_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(StockInfo, slug =slug, active = True)

        try:
            instance = get_object_or_404(StockInfo, slug=slug)
        except StockInfo.DoesNotExist:
            raise Http404("Not Found")
        except StockInfo.MultipleObjectReturned:
            qs = StockInfo.objects.filter(slug=slug, active= True)
            instance = qs.first()
        except:
            raise Http404("Sorry Bro")
        return instance


'''
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(StockInfo, slug=slug)
        if instance is None:
            raise Http404("Product doesn't exist")

        return instance

'''





