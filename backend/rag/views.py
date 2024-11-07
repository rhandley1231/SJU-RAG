from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import conversational_rag  # Updated function name to match utility

@api_view(['POST'])
def ask(request):
    global chat_history
    data = request.data
    question = data.get('question')

    if question:
        result = conversational_rag(question)
        return Response(result)
    
    return Response({'error': 'Invalid question'}, status=400)
