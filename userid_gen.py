from django.utils.crypto import get_random_string
class RandomTokenGenerator:
    def make_id(self):
        return get_random_string(6)

uid = RandomTokenGenerator()