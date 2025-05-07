from api.search import handler, vercel_handler

def lambda_handler(event, context):
    return handler(event, context)

def vercel_handler(request):
    return VercelHandler(request) 