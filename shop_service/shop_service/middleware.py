import logging

logger = logging.getLogger('shop_service')

class DRFLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f'Request: {request.method} {request.get_full_path()}')
        logger.info(f'Headers: {dict(request.headers)}')
        if request.body:
            logger.info(f"Body: {request.body.decode('utf-8')}")

        response = self.get_response(request)
        logger.info(f'Response status: {response.status_code}')
        if hasattr(response, 'data'):
            logger.info(f'Response data: {response.data}')
        else:
            logger.info(f'Response content: {response.content.decode("utf-8")}')
