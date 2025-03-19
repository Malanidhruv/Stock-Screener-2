from pya3 import Aliceblue

def initialize_alice(user_id, api_key):
    """ Initialize AliceBlue API session dynamically."""
    alice = Aliceblue(user_id=user_id, api_key=api_key)
    alice.get_session_id()
    return alice
