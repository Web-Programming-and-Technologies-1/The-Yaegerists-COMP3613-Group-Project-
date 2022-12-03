import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import date, datetime

from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import *

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class ProfileUnitTests(unittest.TestCase):

    def test_new_profile(self):
        profile = Profile(username="bob", email="bob@mail.com", password="bobpass")
        assert profile.username == "bob"

    def test_toJSON(self):
        profile = Profile(username="bob", email="bob@mail.com", password="bobpass")
        profile_json = profile.toJSON()
        self.assertDictEqual(profile_json, {"profileId":None, "username":"bob", "email":"bob@mail.com",  "recipients": [], "feeds": []})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        profile = Profile(username="bob", email="bob@mail.com", password=password)
        assert profile.password != password

    def test_set_password(self):
        password = "bobpass"
        hashed = generate_password_hash(password, method='sha256')
        profile = Profile(username="bob", email="bob@mail.com", password=password)
        assert profile.password != password

    def test_check_password(self):
        password = "mypass"
        profile = Profile(username="bob", email="bob@mail.com", password=password)
        assert profile.check_password(password)

class ImageUnitTests(unittest.TestCase):

    def test_toJSON(self):
        image = Image(profileId=1, url="https://play.google.com/store/apps/dev?id=5700313618786177705&hl=en_US&gl=US")
        image_json = image.toJSON()
        self.assertDictEqual(image_json, {"id":None, "profileId": 1, "url":"https://play.google.com/store/apps/dev?id=5700313618786177705&hl=en_US&gl=US","rankings":[]})

class RatingUnitTests(unittest.TestCase):

    def test_toJSON(self):
        rating = Rating(senderId=1, receiverId=2, score=4)
        rating_json = rating.toJSON()
        self.assertDictEqual(rating_json, {"id":None, "senderId":1, "receiverId": 2, "score":4, "timeStamp": date.today()})

# class RankingUnitTests(unittest.TestCase):

#     def test_toJSON(self):
#         ranking = Ranking()
#         ranking_json = ranking.toJSON()
#         self.assertDictEqual(ranking_json, {"id":None, "rankerId":1, "imageId": 2, "score":3})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

@pytest.mark.run(order=1)
def test_authenticate():
        profile = create_profile(username="bob", email="bob@gmail.com", password="bobpass")
        assert authenticate("bob", "bobpass") != None


class ProfileIntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=2)
    def test_create_user(self):
        profile = create_profile(username="rick", email="rick@mail.com", password="rickpass")
        assert profile.username == "rick"

    @pytest.mark.run(order=3)
    def test_get_all_profiles_json(self):
        profile_json = get_all_profiles_json()
        self.assertListEqual([{"profileId":1, "username":"bob", "email": "bob@gmail.com", "recipients": [],"feeds":[]}, {"profileId":2, "username":"rick", "email": "rick@mail.com", "recipients": [],"feeds":[]}], profile_json)

    @pytest.mark.run(order=4)
    def test_update_profile(self):
        profile = update_profile(profileId=1, username="ronnie", email="ronnie@mail.com", password="ronniepass")
        assert profile.username == "ronnie"

    @pytest.mark.run(order=5)
    def test_delete_profile(self):
        is_deleted = delete_profile(profileId=1)
        assert is_deleted == True

class ImageIntegrationTests(unittest.TestCase):

    @pytest.mark.run(order=6)
    def test_create_image(self):
        image = create_image(profileId=2, url ='https://i.pcmag.com/imagery/reviews/03aizylUVApdyLAIku1AvRV-39.fit_scale.size_760x427.v1605559903.png')
        assert image.imageId == 1

    @pytest.mark.run(order=7)
    def test_get_image_json(self):
        image_json = get_image_json(imageId=1)
        assert {"id":1, "profileId":2, "url":'https://i.pcmag.com/imagery/reviews/03aizylUVApdyLAIku1AvRV-39.fit_scale.size_760x427.v1605559903.png',"rankings":[]} == image_json
       
       
    @pytest.mark.run(order=8)   
    def test_get_images_by_profileId_json(self):
        images_json = get_images_by_profileId_json(profileId=2)
        self.assertListEqual([{"id":1, "profileId":2, "url":'https://i.pcmag.com/imagery/reviews/03aizylUVApdyLAIku1AvRV-39.fit_scale.size_760x427.v1605559903.png',"rankings":[]}],images_json)
       
    @pytest.mark.run(order=9) 
    def test_get_all_images_json(self):
        image = create_image(profileId=2, url="https://media.newyorker.com/photos/6226b3a193b7d1ae15fad583/4:3/w_1032,h_774,c_limit/Chayka_google_v2.gif")
        images_json = get_all_images_json()
        self.assertListEqual([{"id":1, "profileId":2, "url":'https://i.pcmag.com/imagery/reviews/03aizylUVApdyLAIku1AvRV-39.fit_scale.size_760x427.v1605559903.png',"rankings":[]}, {"id":2, "profileId":2, "url":'https://media.newyorker.com/photos/6226b3a193b7d1ae15fad583/4:3/w_1032,h_774,c_limit/Chayka_google_v2.gif',"rankings":[]}], images_json)

    @pytest.mark.run(order=10) 
    def test_update_image(self):
        new_image = update_image(imageId=1, url="https://www.shutterstock.com/image-photo/valencia-spain-march-05-2017-260nw-593204357.jpg")
        assert new_image.url == "https://www.shutterstock.com/image-photo/valencia-spain-march-05-2017-260nw-593204357.jpg"
   
    @pytest.mark.run(order=11) 
    def test_delete_image(self):
        is_deleted = delete_image(id=1)
        assert is_deleted == True
       
class RatingIntegrationTests(unittest.TestCase):

    @pytest.mark.run(order=12) 
    def test_create_rating(self):
        rating = create_rating(senderId=1, receiverId=2, score=4)
        assert rating.ratingId == 1

    @pytest.mark.run(order=13) 
    def test_get_ratings_by_receiver_json(self):
        ratings = get_ratings_by_receiver_json(receiverId=2)
        self.assertListEqual(ratings, [{"id":1, "senderId":1, "receiverId": 2, "score":4, "timeStamp": date.today()}])
    
    @pytest.mark.run(order=14) 
    def test_get_ratings_by_sender_json(self):
        ratings = get_ratings_by_sender_json(senderId=1)
        self.assertListEqual(ratings, [{"id":1, "senderId":1, "receiverId": 2, "score":4, "timeStamp": date.today()}])

    @pytest.mark.run(order=15) 
    def test_get_all_ratings_json(self):
        ratings_json = get_all_ratings_json()
        self.assertListEqual([{"id":1, "senderId":1, "receiverId": 2, "score":4, "timeStamp": date.today()}], ratings_json)

    # @pytest.mark.run(order=16)
    # def test_get_rating_by_actors(self):
    #     rating = get_rating_by_actors(senderId=1, receiverId=2)
    #     assert rating.score == 4

    # def test_update_rating(self):
    #     rating = update_rating(1, 5)
    #     assert rating.score == 5

    # def test_try_calculate_rating(self):
    #     user = create_user("phil", "philpass")
    #     rating = create_rating(user.id, 2, 5)
    #     calculated = get_calculated_rating(2)
    #     assert calculated == 4

    # def test_get_level(self):
    #     assert get_level(1) == 1


# class RankingIntegrationTests(unittest.TestCase):

#     def test_create_rating(self):
#         ranking = create_ranking(1, 2, 3)
#         assert ranking.id == 1

#     def test_get_ranking(self):
#         ranking = get_ranking(1)
#         assert ranking.creatorId == 1

#     def test_get_all_rankings(self):
#         ranking = create_ranking(2, 1, 4)
#         rankingList = []
#         rankingList.append(get_ranking(1))
#         rankingList.append(get_ranking(2))
#         self.assertListEqual(get_all_rankings(), rankingList)

#     def test_get_all_rankings_json(self):
#         rankings_json = get_all_rankings_json()
#         self.assertListEqual([{"id":1, "creatorId":1, "imageId": 2, "score":3}, {"id":2, "creatorId":2, "imageId": 1, "score":4}], rankings_json)

#     def test_get_rankings_by_creatorid(self):
#         rankings = get_rankings_by_creator(2)
#         self.assertListEqual(rankings, [{"id":2, "creatorId":2, "imageId": 1, "score":4}])

#     def test_get_rankings_by_imageid(self):
#         rankings = get_rankings_by_image(2)
#         self.assertListEqual(rankings, [{"id":1, "creatorId":1, "imageId": 2, "score":3}])

#     def test_get_ranking_by_actors(self):
#         ranking = get_ranking_by_actors(1, 2)
#         assert ranking.id == 1

#     def test_update_ranking(self):
#         ranking = update_ranking(1, 5)
#         assert ranking.score == 5

#     def test_try_calculate_ranking(self):
#         ranking = create_ranking(3, 2, 5)
#         calculated = get_calculated_ranking(2)
#         assert calculated == 4


# class DistributionIntegrationTests(unittest.TestCase):
#     pass

# class ProfileFeedIntegrationTests(unittest.TestCase):
#     pass