from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
owner = int(os.getenv('ORG_OWNER'))

print(f"this is the token: {token}")
print(f"this is the owner: {owner} and the type is {type(owner)}")
