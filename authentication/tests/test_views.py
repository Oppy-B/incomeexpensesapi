from .test_setup import TestSetUp
from ..models import User

class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url) #passing post data to the reverse link from test setup and in this case we passed nothing
        #import pdb
        #pdb.set_trace()
        self.assertEqual(res.status_code,400)     # would be a pass because it is a 400 error becasue no user data was passed

    def test_user_can_register_correctly(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json") #passing post data to the reverse link from test setup and in this case we passed userdata
        
        self.assertEqual(res.status_code,201)     # would be a pass because it is a 201 success becasue we pased a user data 
        
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        res = self.client.post(
            self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code,401)

    def test_user_can_login_with_verified_email(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        email = response.data['email']
        user = User.objects.get(email=email)
        user.is_verified=True
        user.save()
        res = self.client.post(
            self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code,200)