from django.shortcuts import render, HttpResponse
import circuitbreaker
from circuitbreaker import circuit
import json,requests
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class MyCircuitBreaker(circuitbreaker.CircuitBreaker):  #creating cusotm circuite breaker
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 30
    EXPECTED_EXCEPTION = requests.RequestException

#@MyCircuitBreaker()  #applying the circuite breaker
#@method_decorator(csrf_exempt,name='dispatch')
@MyCircuitBreaker() 
def call_external():
  BASE_URL = "https://swap1.dev"
  END_POINT = "api/planets/1/"
  resp = requests.get(f"{BASE_URL}/{END_POINT}")
  data = []
  if resp.status_code == 200:
    data = resp.json()
    
  return data


class Test1(APIView):
    
    def post(self,request):
        try:
           
            data = request.data
            print('data is: ',data)
            condition = bool(data['condition'])
            if not condition:
                print('no exceptions')
            else :
                print('applying exception')
                val = call_external()
                raise Exception('An error occured in the function')
            return Response(json.dumps({'success':'no exceptions applyed'}),status=200)
        except Exception as e:
           return Response(json.dumps({'failed': f'Error occurred: {e}'}),status=400)
        
        except :
            return Response(json.dumps({'failed':'error occured'}),status=400)
