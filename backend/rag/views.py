from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import conversational_rag

@api_view(['POST'])
def ask(request):
    data = request.data
    question = data.get('question')
    session_id = data.get('session_id')  # Retrieve session_id if provided

    if question:
        result = conversational_rag(question, session_id)
        return Response(result)
    
    return Response({'error': 'Invalid question'}, status=400)
