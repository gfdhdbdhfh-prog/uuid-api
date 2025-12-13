def handler(request):
    return {
        "status": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "hello": "world",
            "test": "API works!"
        }
    }

