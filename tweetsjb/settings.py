import os
import dotenv

dotenv.load_dotenv(
    dotenv.find_dotenv()
)

class Settings:

    twitter_consumer_token = os.getenv('TWITTER_CONSUMER_TOKEN', None)
    twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', None)
    twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN', None)
    twitter_secret_token = os.getenv('TWITTER_SECRET_TOKEN', None)

    FOLLOW_IDS = [
        '128372940',    # Jair Bolsonaro
        '74756085',     # Eduardo Bolsonaro
        '68712576',     # Carlos Bolsonaro
        '40053694',     # Flavio Bolsonaro
    ]

