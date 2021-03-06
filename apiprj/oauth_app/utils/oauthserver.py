from apiprj.exceptions import AuthError, RequiredParameterDoesNotExist
from apiprj.ext import oauth2
from apiprj.oauth_app import models
from django.core.exceptions import ObjectDoesNotExist

class ServerAlpha(oauth2.Server):
    """Caucse API version implementation of an oauth service provider, based 
    on python-oauth2 Server module.    
    """
    
    def __init__(self, signature_methods=None):
        """Currently this class supports only SHA1 signature."""
        sha1_method = {'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()}
        self.signature_methods = signature_methods or sha1_method

    def _to_oauth_request(self, django_request):
        """This method converts django.http.HttpRequest into oauth.Request
        to process further verification.
        """
        # build auth_header
        auth_header = {}
        if 'Authorization' in django_request.META:
            auth_header = {'Authorization': 
                           django_request.META['Authorization']}
        elif 'HTTP_AUTHORIZATION' in django_request.META:
            auth_header = {'Authorization': 
                            django_request.META['HTTP_AUTHORIZATION']}

        # build parameters, query string
        parameters = dict(django_request.REQUEST)
        qs = django_request.META['QUERY_STRING']

        uri = '%s://%s%s' % (
            django_request.is_secure() and 'https' or 'http',
            django_request.get_host(), 
            django_request.path
        )

        # make oauth.Request object
        request = oauth2.Request.from_request(
            django_request.method,
            uri,
            headers=auth_header,
            parameters=parameters,
            query_string=qs
        )

        return request

    def _fetch_consumer(self, consumer_key):
        try:
            consumer = models.Consumer.objects.get(key=consumer_key)
        except ObjectDoesNotExist as e:
            raise AuthError(e)
        return consumer.to_oauth()

    def _fetch_token(self, token_key):
        try:
            token = models.Token.objects.get(key=token_key)
        except ObjectDoesNotExist as e:
            raise AuthError(e)
        return token.to_oauth()        

    def verify_flow_request(self, django_request):
        """This method converts django request to oauth request and then
        verifies its signature. 
        
        When the request has unknown token or unknown consumer, it will 
        raise Exception.
        """                
        request = self._to_oauth_request(django_request)
        consumer = self._fetch_consumer(request['oauth_consumer_key'])
        token = None
        if 'oauth_token' in request:
            token = self._fetch_token(request['oauth_token'])
        return self.verify_request(request, consumer, token)

    def verify_access_request(self, django_request):
        """This method converts django request to oauth request and then
        verifies its signature. 
        
        When the request has unknown access token or unknown consumer, it
        will raise Exception.
        """
        request = self._to_oauth_request(django_request)
        try:
            request['oauth_consumer_key']
            request['oauth_token']
        except TypeError as e:
            raise RequiredParameterDoesNotExist(e)
        except KeyError as e:
            raise RequiredParameterDoesNotExist(e)
        consumer = self._fetch_consumer(request['oauth_consumer_key'])
        try:
            token = models.Token.objects.get(key=request['oauth_token'])
        except ObjectDoesNotExist as e:
            raise AuthError("no token")
        if token.type != "A":
            raise AuthError("no access token")
        return self.verify_request(request, consumer, token)
