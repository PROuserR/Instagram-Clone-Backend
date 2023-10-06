from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
import stripe
from .serializers import *
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def get_products(request, shop_name):
    products = Product.objects.filter(owner=User.objects.get(username=shop_name))
    serializer = ProductSerializer(products, many=True)
    
    for product in serializer.data:
        image_urls = []
        for image_url in product['images']:
            image_urls.append(str(ProductImage.objects.get(id=image_url)))
        product['images'] = image_urls

    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, product_name):
    product = Product.objects.get(name=product_name)
    serializer = ProductSerializer(product)
    
    image_urls = []
    for image_url in serializer.data['images']:
        image_urls.append(str(ProductImage.objects.get(id=image_url)))


    final_data = serializer.data
    final_data['images'] = image_urls

    return Response(final_data)

@csrf_exempt
@api_view(['POST'])
def create_stripe_checkout_session(request):
    try:
        product_id = request.data['product']
        product=Product.objects.get(id=product_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency':'usd',
                         'unit_amount':int(product.price),
                         'product_data':{
                             'name':product.name,
                             #'images':[f"{API_URL}/{product.product_image}"]
                         }
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id":product.id
            },
            mode='payment',
            success_url=settings.SITE_URL + '?success=true',
            cancel_url=settings.SITE_URL + '?canceled=true',
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)
        customer_email=session['customer_details']['email']
        prod_id=session['metadata']['product_id']
        product=Product.objects.get(id=prod_id)
        #sending confimation mail
        send_mail(
            subject="payment sucessful",
            message=f"thank for your purchase your order is ready.  download url {product.book_url}",
            recipient_list=[customer_email],
            from_email="henry2techgroup@gmail.com"
        )

        #creating payment history
        # user=User.objects.get(email=customer_email) or None

        #PaymentHistory.objects.create(product=product, payment_status=True)
    # Passed signature verification
    return Response(status=200)