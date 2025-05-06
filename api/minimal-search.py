def handler(request, response):
    """Minimal search handler that always succeeds"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": '{"success":true,"mock":true,"complete_quotes":[{"text":"This is a mock quote","sum":123}],"incomplete_quotes":[]}'
    } 