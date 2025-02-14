from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# Create your views here.

from django.http import HttpResponseRedirect

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

def basic(request):
  pdata = {}
  try:
    uid = request.session.get('log_id')
    if uid:
      userdata = login.objects.get(id=uid)
      pdata['userdata'] = userdata
      if userdata.role == "Seller":
        pdata['seller'] = True
    else:
      pdata['userdata'] = None

    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productsview = product_detail.objects.all()
    pdata.update({
      'productsview': productsview,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
    })

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
      pdata['profiledata'] = profiledata
    except customer_detail.DoesNotExist:
      pdata['profiledata'] = None

  except login.DoesNotExist:
    pass

  return pdata


def index(request):
  context = basic(request)
  return render(request, 'index.html',context)

def contact(request):
  context = basic(request)
  if request.method == "POST":
    Name = request.POST.get('Name')
    Email = request.POST.get('Sender')
    Message = request.POST.get('Message')

    if Contact.objects.filter(email=Email).exists():
      messages.error(request, 'you have already filled contact details.')
      return redirect('/contact')
    else:
      contactdata = Contact(name=Name, email=Email, message=Message)
      contactdata.save()
      messages.success(request, 'your contact details is saved.')
      return redirect('/')

  return render(request, 'contact.html',context)

def signin(request):

    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def completeprofile(request):
  try:
    uid = request.session['log_id']
    productsview = product_detail.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    orderdata = product_order.objects.filter(L_id=login(id=uid))

    pdata = {
      'productsview': productsview,
      'profiledata': profiledata,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'orderdata': orderdata,
    }
    return render(request, 'completeprofile.html', pdata)
  except:
    pass
  productsview = product_detail.objects.all()

  details = {
    'productsview': productsview,
  }
  return render(request, 'completeprofile.html', details)

def completeyourprofile(request):
  uid = request.session['log_id']
  if request.method == 'POST':
    uname = request.POST.get("name")
    uaddress = request.POST.get("address")
    udob = request.POST.get("dob")
    file = request.FILES['dp']
    uarea = request.POST.get("areaname")
    ucity = request.POST.get("cityname")
    ustate = request.POST.get("statename")

    userdata = customer_detail(L_id=login(id=uid), Name=uname, Dob=udob, Address=uaddress, dp=file,
                               Area_id=area(id=uarea), City=city(id=ucity), State_id=state(id=ustate))
    userdata.save()
    messages.success(request, 'Data Inserted Successfully.')
    return redirect(index)
  else:
    messages.error(request, 'error occured')

def yourprofile(request):
  try:
    context = basic(request)
    return render(request, 'yourprofile.html', context)
  except:
    pass
  return render(request, 'yourprofile.html')

def forgot(request):
    return render(request, 'forgot.html')


def payment(request):
  return render(request, 'payment.html')


def viewdata(request):
  if request.method == 'POST':
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("confirmpassword")
    role = request.POST.get("usertype")

    if login.objects.filter(Email=email).exists():
      messages.error(request, 'This email is already registerd. Please use another email.')
      return redirect('/')
    else:
      insertdata = login(Email=email, Password=password, Phone=phone, role=role, status="0")
      insertdata.save()

      if role == "Seller":
        messages.info(request,
                      'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
      else:
        messages.success(request, 'Data inserted successfully. You can login now.')

    return redirect('/login')

  return redirect(index)

def checklogin(request):
  if request.method == 'POST':
    username = request.POST['email']
    password = request.POST['password']
    try:
      user = login.objects.get(Email=username, Password=password)
    except login.DoesNotExist:
      user = None

    if user is not None:
      if user.role == "Seller" and user.status == "0":
        print(user.role)
        print(user.status)
        messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
      else:
        request.session['log_id'] = user.id
        request.session.save()
        messages.success(request, 'Login successful...')
        return redirect('/')
    else:
      messages.error(request, 'Invalid Email Id and Password. Please try again.')
      return redirect('/login')
  return render(request, 'login.html')


def logout(request):
    try:
        del request.session['log_id']
    except:
        pass
    return redirect(index)

def forgotpassword(request):
  if request.method == 'POST':
    username = request.POST['email']
    try:
      user = login.objects.get(Email=username)

    except login.DoesNotExist:
      user = None
    # if user exist then only below condition will run otherwise it will give error as described in else condition.
    if user is not None:
      #################### Password Generation ##########################
      import random
      letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
      numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
      symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

      nr_letters = 6
      nr_symbols = 1
      nr_numbers = 3
      password_list = []

      for char in range(1, nr_letters + 1):
        password_list.append(random.choice(letters))

      for char in range(1, nr_symbols + 1):
        password_list += random.choice(symbols)

      for char in range(1, nr_numbers + 1):
        password_list += random.choice(numbers)

      print(password_list)
      random.shuffle(password_list)
      print(password_list)

      password = ""  # we will get final password in this var.
      for char in password_list:
        password += char

      ##############################################################

      msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

      ############ code for sending mail ########################

      from django.core.mail import send_mail

      send_mail(
        'Your New Password',
        msg,
        'krushanuinfolabz@gmail.com',
        ['krushanu.vadgama@gmail.com'],
        fail_silently=False,
      )
      # NOTE: must include below details in settings.py
      # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
      # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      # EMAIL_HOST = 'smtp.gmail.com'
      # EMAIL_USE_TLS = True
      # EMAIL_PORT = 587
      # EMAIL_HOST_USER = 'mail from which email will be sent'
      # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

      #############################################

      # now update the password in model
      cuser = login.objects.get(Email=username)
      cuser.Password = password
      cuser.save(update_fields=['Password'])

      print('Mail sent')
      messages.info(request, 'mail is sent')
      return redirect(index)

    else:
      messages.info(request, 'This account does not exist')
  return redirect(index)

def shop(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    productsview = product_detail.objects.all()

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.all()

    # Paginate items
    items_per_page = 4
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'items_page': items_page
    }

    return render(request, 'shop.html', pdata)
  except:
    pass
  productdetails = product_detail.objects.all()
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.all()

  # Paginate items
  items_per_page = 4
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)
  details = {
    'productdetails': productdetails,
    'items_page': items_page,
  }
  return render(request, 'shop.html', details)

def categorywiseproduct(request, pcid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

    # Paginate items
    items_per_page = 3
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'productdetails': productdetails,
      'items_page': items_page,

    }
    return render(request, 'categorywiseproduct.html', details)
  except:
    pass
  productdetails = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

  # Paginate items
  items_per_page = 3
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)


  context = basic(request)
  context.update({'productdetails': productdetails, 'items_page': items_page,})
  return render(request, 'categorywiseproduct.html', context)

def subcategorywiseproduct(request, pscid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

    # Paginate items
    items_per_page = 3
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)



    context = basic(request)
    context.update({'productdetails': productdetails, 'items_page': items_page, })
    return render(request, 'subcategorywiseproduct.html', context)

  except:
    pass
  productdetails = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

  # Paginate items
  items_per_page = 3
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)



  context = basic(request)
  context.update({'productdetails': productdetails, 'items_page': items_page, })
  return render(request, 'subcategorywiseproduct.html', context)


def productView(request, myid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.get(id=myid)

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    context = basic(request)
    context.update({'productdetails': productdetails, })
    return render(request, 'single.html', context)
  except:
    pass
  productdetails = product_detail.objects.get(id=myid)
  details = {
    'productdetails': productdetails,
  }
  return render(request, 'single.html', details)

def addtowishlist(request, awid):
  uid = request.session['log_id']

  try:
    wl = product_wishlist.objects.get(Product_id=product_detail(id=awid), L_id=login(id=uid))

  except product_wishlist.DoesNotExist:
    wl = None

  if wl is None:
    wldata = product_wishlist(Product_id=product_detail(id=awid), L_id=login(id=uid))
    wldata.save()
    messages.success(request, 'Added to Wishlist.')
  else:
    messages.error(request, 'Already added to Wishlist.')

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def wishlists(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    wishlistdata = product_wishlist.objects.filter(L_id=uid)

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'wishlistdata': wishlistdata,
    }


    return render(request, 'wishlist.html',pdata)
  except:
    pass
  return render(request, 'wishlist.html')

def removewish(request, dwid):
  product_wishlist.objects.filter(Product_id=product_detail(id=dwid)).delete()

  return redirect(wishlists)

def addtocart(request):
  try:
    if request.session.is_empty():
      messages.error(request, "Please login")
      return redirect(index)
    else:
      try:
        if request.method == 'POST':
          cartname = request.POST.get("pname")
          cartprice = request.POST.get("amount")
          cartquantity = request.POST.get("quant[1]")
          proid = request.POST.get("pid")
          finalprice = int(cartprice) * int(cartquantity)

          uid = request.session['log_id']
          print(uid)

          existitem = product_cart.objects.filter(L_id=login(id=uid), Product_id=product_detail(id=proid), Order_status=0).first()

          if existitem:
            existitem.Quantity += int(cartquantity)
            existitem.save()
            messages.success(request, 'Your product added in the cart')

          else:
            cartdata = product_cart(Product_id=product_detail(id=proid), L_id=login(id=uid), Product_name=cartname,
                                    Price=cartprice, Quantity=cartquantity,
                                    Final_price=finalprice)
            print("check1")
            cartdata.save()
            messages.success(request, 'Product is added to Cart.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
        pass
      messages.error(request, "Please login")
      return redirect(index)
  except:
    pass
  messages.error(request, "Please login")
  return redirect(index)

from django.db.models import Sum


def Cart(request):
  uid = request.session['log_id']
  logdetail = login.objects.all()
  statedetail = state.objects.all()
  citydetail = city.objects.all()
  areadetail = area.objects.all()

  try:
      profiledata = customer_detail.objects.get(L_id=uid)
  except customer_detail.DoesNotExist:
      profiledata = None


  # cartitems = CART_TABLE.objects.all()
  cartitems = product_cart.objects.filter(L_id=uid, Order_status=0)

  carttotal = cartitems.aggregate(Sum("Final_price"))["Final_price__sum"]
  if carttotal is None:
    carttotal = 0

  # Add shipping charge
  shipping_charge = 100
  total_amount = carttotal + shipping_charge

  print(carttotal)
  uname = customer_detail.objects.filter(L_id=login(id=uid))

  cartview = {
    'cartitems': cartitems,
    'carttotal': carttotal,
    'uname': uname,
    'total_amount': total_amount,
    'shipping_charge': shipping_charge,
    'logdetail': logdetail,
    'statedetail': statedetail,
    'citydetail': citydetail,
    'areadetail': areadetail,
    'profiledata': profiledata,
  }

  return render(request, 'cart.html', cartview)

def increaseitem(request, id):
  try:
    cart_data = product_cart.objects.get(id=id, Order_status=0)
    if cart_data.Quantity >= 0:
      cart_data.Quantity += 1
      cart_data.Final_price += cart_data.Product_id.Pro_price
      cart_data.save()
      return redirect('cart')
  except product_cart.DoesNotExist:
    pass
  return render(request, "cart.html")

def decreaseitem(request, id):
  try:
    cart_data = product_cart.objects.get(id=id, Order_status=0)
    if cart_data.Quantity > 0:
      cart_data.Quantity -= 1
      cart_data.Final_price -= cart_data.Product_id.Pro_price
      cart_data.save()
      if cart_data.Quantity == 0:
        cart_data.delete()
      return redirect('cart')
  except product_cart.DoesNotExist:
    pass
  return render(request, "cart.html")
def RemoveFromCart(request, did):
  product_cart.objects.filter(id=did).delete()

  cartitems = product_cart.objects.all()
  carttotal = product_cart.objects.aggregate(Sum("Final_price"))
  carttotal = carttotal.get("Final_price__sum")

  print(carttotal)
  uid = request.session['log_id']
  uname = customer_detail.objects.filter(L_id=login(id=uid))

  context = {
    'cartitems': cartitems,
    'carttotal': carttotal,
    'uname': uname,
  }

  return redirect(Cart)

def OrderComplete(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    address = request.POST.get("address")
    uid = request.session['log_id']
    cust_detail = customer_detail.objects.get(L_id=login(id=uid))

    if address == "":
      address = cust_detail.Address

    paymentopt = request.POST.get("payment")
    print(paymentopt)
    if paymentopt == "online":
      return render(request, 'payment.html')
    else:
      carttotal = product_cart.objects.filter(L_id=uid, Order_status=0).aggregate(Sum("Final_price"))
      carttotal = carttotal.get("Final_price__sum")
      orderdata = product_order(L_id=login(id=uid), Address=address, Total_amount=carttotal+float(100),
                                Payment_status=paymentopt, order_status='placed')
      orderdata.save()

      lasstid = product_order.objects.latest('id')

      print(lasstid)

      objid = lasstid.id
      print(objid)

      obj = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
      for object in obj:
        object.Order_id = objid
        object.Order_status = 1
        object.save()

      messages.success(request, 'Order Placed Successfully.')
      return redirect(yourorders)

  return render(request, 'orderplaced.html')

def verifypayment(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    card_number = request.POST.get("number")
    card_cvv = request.POST.get("security-code")
    exp_date = request.POST.get("expiration-month-and-year")

    carddetail = card_detail.objects.get()

    ocn = carddetail.card_number
    ocvv = carddetail.card_cvv
    oexpd = carddetail.exp_date
    cb = carddetail.card_balance
    carttotal = product_cart.objects.aggregate(Sum("Final_price"))
    carttotal = carttotal.get("Final_price__sum")

    if ocn == card_number and ocvv == card_cvv and oexpd == exp_date:
      print("payment expected")
      cb = cb - carttotal
      carddetail.card_balance = cb
      carddetail.save(update_fields=['card_balance'])
      uid = request.session['log_id']
      cust_detail = customer_detail.objects.get(L_id=login(id=uid))
      custadd = cust_detail.Address
      orderdata = product_order(L_id=login(id=uid), Address=custadd, Total_amount=carttotal+float(100),
                                Payment_status="online", order_status='placed')
      orderdata.save()

      lasstid = product_order.objects.latest('id')

      print(lasstid)

      objid = lasstid.id
      print(objid)

      obj = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
      for object in obj:
        object.Order_id = objid
        object.Order_status = 1
        object.save()

      messages.success(request, 'Payment Successfull.')
      return redirect(yourorders)

    else:
      messages.error(request, 'Payment failed. Wrong payment details')
      return redirect(Cart)

  return render(request, 'payment.html')

def yourorders(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    orderdata = product_order.objects.filter(L_id=uid)

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'profiledata': profiledata,
      'orderdata': orderdata,
    }

    return render(request, 'yourorders.html', pdata)
  except:
    pass
  return render(request, 'yourorders.html')


def yourordersingle(request, yoid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    cartdetail = product_cart.objects.filter(Order_id=yoid)

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'cartdetail': cartdetail,

    }
    return render(request, 'yourordersingle.html', details)
  except:
    pass
  return render(request, 'yourordersingle.html')

def productfeedback(request, product_id):
    context = basic(request)
    context.update({"productid": product_id})
    return render(request, 'feedback.html', context)

def storefeedback(request):
  context = basic(request)
  user_id = request.session['log_id']
  if request.method == 'POST':
    ratings = request.POST.get('ratings')
    feedback_message = request.POST.get('feedback_message')
    product_id = request.POST.get('productid')

    if Feedback.objects.filter(L_id=user_id, Product_id=product_id).exists():
      messages.error(request, 'you have already filled feedback.')
      return redirect('/')
    else:
      print(product_id)
      print(user_id)
      insertfeedback = Feedback(L_id=login(id=user_id),Product_id=product_detail(id=product_id), ratings=ratings,comment=feedback_message,
        )
      insertfeedback.save()
      messages.success(request, "feedback is submitted")
      return redirect(yourorders)
  return render(request, 'index.html', context)

def submitproduct(request):
  context = basic(request)
  uid = request.session['log_id']
  categories = product_category.objects.all()
  subcategories = product_subcategory.objects.all()
  if request.method == 'POST':
    category_id = request.POST.get('Product Category')
    sub_id = request.POST.get("Product Subcategory")
    name = request.POST.get('Product Name')
    price = request.POST.get('Product Price')
    desc = request.POST.get('Product Description')
    image = request.FILES.get('Product Image')
    customizable = request.POST.get('customizable', False) == 'True'

    # Create or update Product instance
    category = product_category.objects.get(id=category_id)
    subcategory = product_subcategory.objects.get(id=sub_id)

    product = product_detail(Seller=login(id=uid), Pro_Cat=category, Pro_Subcat=subcategory,Pro_name=name, Pro_description=desc, Pro_price=price, Pro_image=image, is_customizable=customizable)
    product.save()
    messages.success(request, 'product added successfully')
    return redirect(index)

  context.update({'catdata': categories, 'subcatdata':subcategories})
  return render(request,'addproduct.html', context)

def sellerproduct(request):
  context = basic(request)
  uid = request.session['log_id']  # Assuming you have user authentication
  products = product_detail.objects.filter(Seller=uid)

  context.update({"productdetails": products})
  return render(request, 'sellershowproduct.html', context)

def editproductseller(request, product_id):
  context = basic(request)
  uid = request.session['log_id']

  # Fetch the product details
  try:
    product = product_detail.objects.get(id=product_id, Seller=uid)
  except product_detail.DoesNotExist:
    # Handle the case where the product does not exist or does not belong to the seller
    # You can redirect the user to a relevant page or show an error message
    return redirect('/')  # Redirect to homepage for now

  # Pass the product details to the template context
  allcategory = product_category.objects.all()
  allsubcategory = product_subcategory.objects.all()
  context['data'] = product
  context['subcatdata'] = allsubcategory
  context['catdata'] = allcategory

  return render(request, 'edit.html', context)

def updateselller(request, product_id):
  # Assuming you are passing the product ID in the URL

  # Retrieve the product object from the database

  if request.method == 'POST':
    # Update the product details based on the form submission
    Name = request.POST.get('Product Name')
    Description = request.POST.get('Product Description')
    Price = request.POST.get('Product Price')
    Category = request.POST.get('Product Category')
    SubCategory = request.POST.get('Product Subcategory')
    product = product_detail.objects.get(id=product_id)
    product.Pro_name = Name
    product.Pro_description = Description
    product.Pro_price = Price
    product.Pro_Cat = product_category(id=Category)
    product.Pro_Subcat = product_subcategory(id=SubCategory)

    if 'Product Image' in request.FILES:
      file = request.FILES['Product Image']
      product.Pro_image = file
    # Save the updated product object
    product.save()

    # Optionally, you can add a success message
    messages.success(request, 'Product updated successfully.')

    # Redirect to a success page or the product detail page
    return redirect('editproductseller', product_id=product_id)
  else:
    # If it's a GET request, render the form to edit the product
    return render(request, 'edit.html')

def deleteProduct(request, eid):
  object = product_detail.objects.get(id=eid)
  object.delete()
  messages.success(request, "Product Deleted !")
  return redirect(index)

def sellershoworder(request):
  context = basic(request)

  uid = request.session['log_id']
  sellers_products = product_detail.objects.filter(Seller=login(id=uid))
  getdetails = product_cart.objects.filter(Product_id__in=sellers_products, Order_status=1)
  context.update({
    "sellerorderdetails": getdetails,
  })
  return render(request, 'sellershoworder.html', context)

def submitcomplaint(request):
  context = basic(request)

  uid = request.session['log_id']
  if request.method == "POST":
    subject1 = request.POST.get('subject')
    email1 = request.POST.get('email')
    desc1 = request.POST.get('Description')

    insertcomplaint = Complaint(L_id=login(id=uid), subject=subject1, email=email1, description=desc1)
    insertcomplaint.save()
    messages.success(request, "your complaint has been saved")
    return redirect(index)
  return render(request,'Complaint.html', context)
