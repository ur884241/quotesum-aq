from api.search import handler, VercelHandler

def lambda_handler(event, context):
    return handler(event, context)

def vercel_handler(request):
    return VercelHandler(request) 