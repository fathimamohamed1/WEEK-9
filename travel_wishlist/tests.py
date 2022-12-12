from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase): #testing the homepage 

    def test_home_page_shows_empty_list_message_for_empty_databse(self):
        home_page_url= reverse('place_list') 
        response = self.client.get(home_page_url) # saving the response from the test case request
        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html') #making assertions to check if the right template was used 
        self.assertContains(response, 'You have no places in your wishlist') # checking for content and providing a response message 


class TestWishList(TestCase):

    fixtures =['test_places']
    def test_wishlist_contains_not_visited_places(self):
        response =self.client.get(reverse('place_list'))
        self.assertTemplateUsed('travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'Moab')
        self.assertNotContains(response, 'San Francisco')


    
class TestVisitedPage(TestCase): #testing the places visited
    def test_visited_page_shows_empty_list_message_for_empty_databse(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response,'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet') # checking for content and providing a response message 



class VisitedList(TestCase): #testing the places visited 

    fixtures =['test_places']
    def test_visted_list_shows_visited_places(self):
        response =self.client.get(reverse('places_visited'))
        self.assertTemplateUsed('travel_wishlist/visited.html')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Moab')
        self.assertContains(response, 'San Francisco')

    

class TestAddNewPlace(TestCase): #testing for when we add a  new place 

    def test_add_new_unvisited_place(self):
        add_place_url=reverse('place_list')
        new_place_data ={'name': 'Dubai', 'visited' :False}

        response =self.client.post(add_place_url,new_place_data,follow=True)
        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html')

        response_places= response.context['places']
        self.assertEqual(1, len(response_places)) #this only checks one place
        dubai_from_response=response_places[0]

        dubai_from_database=Place.objects.get(name='Dubai', visited= False)

        self.assertEqual(dubai_from_database, dubai_from_response)


class TestVisitedPlace(TestCase):
    fixtures= ['test_places']

    def test_visit_place(self):
        visit_place_url =reverse('place_was_visited', args=(2, ))
        response =self.client.post(visit_place_url,follow=True)

        self.assertTemplateUsed(response , 'travel_wishlist/wishlist.html')
        
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york=Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)


    def test_non_existent_place(self):
        visit_non_existent_place_url =reverse('place_was_visited',args=(98765, ))
        response=self.client.post(visit_non_existent_place_url, follow=True)
        self.assertEqual(404,response.status_code)