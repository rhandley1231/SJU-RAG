from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import your_rag_function  # Import the function from utils

@api_view(['POST'])
def rag_query(request):
    query = request.data.get('query')
    
    if query:
        # Use your_rag_function to process the query
        result = your_rag_function(query)
        return Response({'result': result})
    
    return Response({'error': 'Invalid query'}, status=400)
