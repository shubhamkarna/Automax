from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing, LikedListing
from .forms import ListingForm
from users.forms import Location_form
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from .filters import ListingFilter

# Create your views here.
def main_view(request):
    return render(request, 'views/main.html')


@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    return render(request, 'views/home.html', context={
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
        })

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = Location_form(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(request, f' {listing.model} Listing Posted Successfully')
                return redirect('home')
            else:
                raise Exception    
        except Exception as e:
            print(e)
            messages.error(request,'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = Location_form()
    return render(request, 'views/list.html', context={'listing_form': listing_form, 'location_form': location_form})


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'views/listing_view.html', context={'listing': listing})
    except Exception as e:
        messages.error(request, e)
        print(e)
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = Location_form(request.POST, instance=listing.location)    
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.success(request, f'Listing {id} updated successfully')
                return redirect('home')
            else:
                messages.error(request, f"An error just occured trying to edit the listing.")
                
        else:
            listing_form = ListingForm(instance=listing)
            location_form = Location_form(instance=listing.location)
            context = {
                'listing_form': listing_form,
                'location_form': location_form,
            }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(request, f"An error just occured trying to access the edit page.")
        return redirect('home')



@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

    # if not created i.e. already existed then delete.
    # double like garyo bhani dislike garni banauni
    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })

@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.username} is interested in {listing.model}'
        emailMessage = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on AutoMax'
        send_mail(emailSubject, emailMessage, 'noreply@automax.com',
                  [listing.seller.user.email, ], fail_silently=True)
        return JsonResponse({
            "success": True,
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "info": e,
        })