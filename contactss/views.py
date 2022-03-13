from django.shortcuts import redirect, render
from .models import Contact
from django.core.mail import send_mail
from django.contrib import messages


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = Contact.objects.all().filter(
            listing_id=listing_id, user_id=user_id)
        if has_contacted:
            messages.error(request, 'you had make a contact for this property')
            return redirect('/listings/'+listing_id)
    contact = Contact(listing_id=listing_id, listing=listing,
                      name=name, email=email, phone=phone, message=message,
                      user_id=user_id)
    contact.save()

    # email send
    send_mail(
        'listing inquiry',
        'your inquiry is about ' + listing + '. sign in to your account and dashboard',
        'ertye2956@gmail.com',
        ['dfghd2956@gmail.com'],
        fail_silently=False
    )
    messages.success(request, 'your contact saved')
    return redirect('/listings/'+listing_id)
    # Create your views here.
