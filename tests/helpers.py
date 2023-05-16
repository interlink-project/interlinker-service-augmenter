
class MockConsumer(object):
    def __init__(self, key=''):
        self.key = key
        self.secret = 'yourconsumersecret'
        self.ttl = 86400

class MockUser(object):
    def __init__(self, userid='alice', consumer=None):
        self.id = userid
        self.consumer = MockConsumer(consumer if consumer is not None else '')
        self.is_admin = False


class MockAuthenticator(object):
    def request_user(self, request):
        return MockUser()

def mock_authorizer(*args, **kwargs):
    return True
