from api.search import vercel_handler

def handler(event, context):
    return vercel_handler(event) 