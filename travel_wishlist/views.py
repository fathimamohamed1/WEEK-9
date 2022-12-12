from django.shortcuts import render , redirect , get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages



@login_required
def place_list(request):

    if request.method =='POST':
        form =NewPlaceForm(request.POST) # this is creating a form from data 
        place= form.save(commit=False) # its creating a model object from form 
        place.user = request.user
        if form.is_valid: # validation against databse constraints
            place.save() #saves place to database
            return redirect('place_list') # this redirects to the wishlist places


    places=Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form=NewPlaceForm()
    return render (request, 'travel_wishlist/wishlist.html', {'places':places, 'new_place_form':new_place_form})
@login_required
def places_visited(request): # list of places that have been visited
    visited= Place.objects.filter(visited=True)
    return render (request, 'travel_wishlist/visited.html',{'visited':visited})  

@login_required
def place_was_visited(request,place_pk):
    if request.method =='POST':
        #place =Place.objects.get(pk=place_pk) #this is a database query that helps getting the single object that is needed 
        place= get_object_or_404(Place, pk=place_pk) # if not visited and doesnt exist it should show 404 error message
        if place.user == request.user: # if place user is equal to request user ot will return place visited and save it else it will return httpforbiden
            place.visited = True  
            place.save() # saves to the database

        else:
            return HttpResponseForbidden
        return redirect('place_list')  # redirects to the wishlist places 
@login_required
def about(request): # about page 
    author ='Fathima' 
    about= 'A website to create a list of places to visit'
    return render(request,'travel_wishlist/about.html' , {'author': author, 'about': about})

@login_required
def place_details(request,place_pk):
    place= get_object_or_404(Place, pk=place_pk)


    if place.user !=request.user: #checking to see if this belongs to the current user and if not return httpresponseforbidden
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid(): #istheformvalid
            form.save()
            messages.info(request, 'Trip information updated.')
        else:
            messages.error (request, form.errors) 

        return redirect('place_details', place_pk=place_pk)

    else:
        if place.visited:
            review_form =TripReviewForm(instance=place)
            return render (request,'travel_wishlist/place_detail.html',{'place':place, 'review_form':review_form})

        else:
            return render (request,'travel_wishlist/place_detail.html',{'place':place})


@login_required
def delete_place(request,place_pk):
    place =get_object_or_404(Place, pk=place_pk)
    if place.user == request.user :
        place.delete()
        return redirect('place_list')

    else:
        return HttpResponseForbidden()
