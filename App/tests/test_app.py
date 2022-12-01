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
# class UserUnitTests(unittest.TestCase):

#     def test_new_user(self):
#         user = User("bob", "bobpass")
#         assert user.username == "bob"

#     def test_toJSON(self):
#         user = User("bob", "bobpass")
#         user_json = user.toJSON()
#         self.assertDictEqual(user_json, {"id":None, "username":"bob", "images": [], "ratings": []})
    
#     def test_hashed_password(self):
#         password = "mypass"
#         hashed = generate_password_hash(password, method='sha256')
#         user = User("bob", password)
#         assert user.password != password

#     def test_check_password(self):
#         password = "mypass"
#         user = User("bob", password)
#         assert user.check_password(password)

# class ImageUnitTests(unittest.TestCase):

#     def test_new_image(self):
#         image = Image(1)
#         assert image.rankings == []

#     def test_toJSON(self):
#         image = Image(1)
#         image_json = image.toJSON()
#         self.assertDictEqual(image_json, {"id":None, "rankings":[], "userId": 1})

# class RatingUnitTests(unittest.TestCase):

#     def test_new_rating(self):
#         rating = Rating(1, 2, 3)
#         assert rating.score == 3

#     def test_toJSON(self):
#         rating = Rating(1, 2, 3)
#         rating_json = rating.toJSON()
#         self.assertDictEqual(rating_json, {"id":None, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()})

# class RankingUnitTests(unittest.TestCase):

#     def test_new_ranking(self):
#         ranking = Ranking(1, 2, 3)
#         assert ranking.score == 3

#     def test_toJSON(self):
#         ranking = Ranking(1, 2, 3)
#         ranking_json = ranking.toJSON()
#         self.assertDictEqual(ranking_json, {"id":None, "creatorId":1, "imageId": 2, "score":3})

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
       
# class RatingIntegrationTests(unittest.TestCase):

#     def test_create_rating(self):
#         rating = create_rating(1, 2, 3)
#         assert rating.id == 1

#     def test_get_rating(self):
#         rating = get_rating(1)
#         assert rating.creatorId == 1

#     def test_get_all_ratings(self):
#         rating = create_rating(2, 1, 4)
#         ratingList = []
#         ratingList.append(get_rating(1))
#         ratingList.append(get_rating(2))
#         self.assertListEqual(get_all_ratings(), ratingList)

#     def test_get_all_ratings_json(self):
#         ratings_json = get_all_ratings_json()
#         self.assertListEqual([{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}, {"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}], ratings_json)

#     def test_get_ratings_by_creatorid(self):
#         ratings = get_ratings_by_creator(2)
#         self.assertListEqual(ratings, [{"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}])

#     def test_get_ratings_by_targetid(self):
#         ratings = get_ratings_by_target(2)
#         self.assertListEqual(ratings, [{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}])

#     def test_get_rating_by_actors(self):
#         rating = get_rating_by_actors(1, 2)
#         assert rating.id == 1

#     def test_update_rating(self):
#         rating = update_rating(1, 5)
#         assert rating.score == 5

#     def test_try_calculate_rating(self):
#         user = create_user("phil", "philpass")
#         rating = create_rating(user.id, 2, 5)
#         calculated = get_calculated_rating(2)
#         assert calculated == 4

#     def test_get_level(self):
#         assert get_level(1) == 1


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