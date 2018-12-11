from django.shortcuts import render, redirect, render_to_response
from .models import Trade
from stock_info.models import StockInfo
from orders.models import Order
from billing.models import BillingPortfolio
from .models import Trade
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template import RequestContext


User = settings.AUTH_USER_MODEL
from django.db import connection
#print (connection.queries)



def trade_home(request):
    trade_obj, new_obj = Trade.objects.new_or_get(request)

    p = get_object_or_404(Trade, pk=trade_obj.id)
    print(p)
    if request.method == 'POST':
        share_amount_form = TradeForm(request.POST or None, instance=p)
        print(share_amount_form.is_valid())
        if share_amount_form.is_valid():
            # share_amount = share_amount_form.save()
            share_amount_form.save()

    else:
        share_amount_form = TradeForm(instance=p)





    #
    # p = get_object_or_404(Trade)
    # if True:
    #     if request.method == 'POST':
    #         share_amount_form = TradeForm(request.POST or None, instance=p)
    #         print(share_amount_form.is_valid())
    #         if share_amount_form.is_valid():
    #             # share_amount = share_amount_form.save()
    #             share_amount_form.save()
    #
    #     else:
    #         share_amount_form = TradeForm(instance=p)
    #
    #     return render_to_response("stock_trade/trade_home.html", {'Trade': p, 'form': share_amount_form},
    #                               context_instance=RequestContext(request))



    return render(request, "stock_trade/trade_home.html", {"trade":trade_obj})




def trade_update(request):
    print(request.POST)
    stock_info_id = request.POST.get("stock_info_id")
    if stock_info_id is not None:
        try:

            stock_info_obj = StockInfo.objects.get(id=stock_info_id)
        except StockInfo.DoesNotExist:
            print("show message of trading")
            return redirect("trade:home")

        trade_obj, new_obj = Trade.objects.new_or_get(request)
        if stock_info_obj in trade_obj.stock_info.all():
            trade_obj.stock_info.remove(stock_info_obj)



        else:
            trade_obj.stock_info.add(stock_info_obj)
        # trade_obj.symbol = "add"
        # trade_obj
        request.session['trade_items'] = trade_obj.stock_info.count()

    return redirect("trade:home")#redirect(stock_info_obj.get_absolute_url())


# from .models import Trade
# from stock_info.models import StockInfo
#
# def add_to_cart(request, product_id, quantity):
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     cart.add(product, product.unit_price, quantity)
#
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     cart.remove(product)
#
# def get_cart(request):
#     return render_to_response('cart.html', dict(cart=Cart(request)))


def checkout_home(request):

    trade_obj, trade_created = Trade.objects.new_or_get(request)
    order_obj = None
    if trade_created or trade_obj.stock_info.count() == 0:
        return redirect("trade:home")


    # user = request.user
    # billing_portfolio = None
    billing_portfolio, billing_portfolio_created = BillingPortfolio.objects.new_or_get(request)


    # if user.is_authenticated:
    #     billing_portfolio, billing_portfolio_created = BillingPortfolio.objects.get_or_create(user=user,
    #                                                                                    email=user.email)
    # else:
    #     pass

    if billing_portfolio is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_portfolio, trade_obj)
        # order_obj.save()

        # order_qs = Order.objects.filter(trade = trade_obj)
        # if order_qs.exists():
        #     order_qs.update(active= False)
        # else:
        #     order_obj= Order.objects.create(billing_portfolio = billing_portfolio, trade=trade_obj)


    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['trade_items'] = 0
            del request.session['trade_id']
        #del request.session['trade_id']
            return redirect("trade:success")

    # del request.session['trade_id']
    # update order_obj to done, "paid"
    # redirect to success page

    context = {
        "object": order_obj,
        "billing_portfolio": billing_portfolio
    }
    return render(request, "stock_trade/checkout.html", context)


def checkout_done_view(request):
    return render(request,"stock_trade/checkout-done.html", {} )





#
#
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Trade
from .forms import TradeForm




def share_amount(request):
    # trade_obj= Trade.objects.new_or_get(request)

    p = get_object_or_404(Trade, pk =145)
    print(p)
    if request.method == 'POST':
        share_amount_form = TradeForm(request.POST or None, instance=p)
        print(share_amount_form.is_valid())
        if share_amount_form.is_valid():
            #share_amount = share_amount_form.save()
            share_amount_form.save()

    else:
        share_amount_form = TradeForm(instance=p)


    #return redirect("trade:home")
    return render_to_response("stock_trade/share_amount.html", {'Trade': p, 'share_amount_form': share_amount_form})

    # return render_to_response("stock_trade/share_amount.html",{'share_amount_form': share_amount_form})
#     # create a form instance and populate it with data from the request:
#     form = TradeForm(request.POST)
#     # check whether it's valid:
#     if form.is_valid():
#         # process the data in form.cleaned_data as required
#         p = form.save()
#         '''
#         name = form.cleaned_data['name']
#         number = form.cleaned_date['phone_number']
#         p = Person(name=name, phone_number=number, date_subscribed=datetime.now(), messages_recieved=0)
#         p.save()
#         '''
#         # redirect to a new URL:
#         return HttpResponseRedirect('/success/')
#   # if a GET (or any other method) we'll create a blank form
#   else:
#     form = TradeForm()
#
#   return render(request, "stock_trade/trade_home.html", {'form': form}, context_instance=RequestContext(request))
