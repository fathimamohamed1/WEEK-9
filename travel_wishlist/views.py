from django.shortcuts import render , redirect , get_object_or_404
from .models import Place
from .forms import NewPlaceForm

def place_list(request):

    if request.method =='POST':
        form =NewPlaceForm(request.POST) # this is creating a form from data 
        place= form.save() # its creating a model object from form 
        if form.is_valid: # validation against databse constraints
            place.save() #saves place to database
            return redirect('place_list') # this redirects to the wishlist places


    places=Place.objects.filter(visited=False).order_by('name')
    new_place_form=NewPlaceForm()
    return render (request, 'travel_wishlist/wishlist.html', {'places':places, 'new_place_form':new_place_form})
  
def places_visited(request): # list of places that have been visited
    visited= Place.objects.filter(visited=True)
    return render (request, 'travel_wishlist/visited.html',{'visited':visited})  


def place_was_visited(request,place_pk):
    if request.method =='POST':
        #place =Place.objects.get(pk=place_pk) #this is a database query that helps getting the single object that is needed 
        place= get_object_or_404(Place, pk=place_pk) # if not visited and doesnt exist it should show 404 error message
        place.visited = True  
        place.save() # saves to the database
        return redirect('place_list')  # redirects to the wishlist places 

def about(request): # about page 
    author ='Fathima' 
    about= 'A website to create a list of places to visit'
    return render(request,'travel_wishlist/about.html' , {'author': author, 'about': about})

