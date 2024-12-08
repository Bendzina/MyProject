from django.utils.deprecation import  MiddlewareMixin
import logging

logger = logging.getLogger(__name__)



class SimpleMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        logger.info(f'start Processing request:{request.path}')

        response = self.get_response(request)
    

        logger.info(f'Finished processing request:{request.path}')

        return response
    
    def process_exception(self, request, exception):
        logger.error(f'Exception occurred: {request.path} - {exception}')

    