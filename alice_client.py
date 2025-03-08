from pya3 import Aliceblue
from config import get_user_credentials

def initialize_alice():
    """ Initialize AliceBlue API session."""
    user_id, api_key = get_user_credentials()
    alice = Aliceblue(user_id=user_id, api_key=api_key)
    alice.get_session_id()
    return alice
