from pya3 import Aliceblue

def initialize_alice(user_id, api_key):
    """Initialize AliceBlue API session with user-provided credentials."""
    alice = Aliceblue(user_id=user_id, api_key=api_key)
    alice.get_session_id()  # Authenticate session
    return alice
