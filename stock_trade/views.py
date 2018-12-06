from django.shortcuts import render, redirect
from .models import Trade
from stock_info.models import StockInfo
from orders.models import Order



from django.db import connection
#print (connection.queries)



def trade_home(request):
    trade_obj, new_obj = Trade.objects.new_or_get(request)
    #stock_info = trade_obj.stock_info.all()
    # #print (stock_info.query)
    # #print(stock_info)
    # estimated_cost = 0
    # for x in stock_info:
    #     estimated_cost += x.open
    # #print(estimated_cost)
    #
    # trade_obj.estimated_cost = estimated_cost
    # trade_obj.save()
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
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(trade = trade_obj)
    return render(request, "stock_trade/checkout.html", {"object": order_obj})

