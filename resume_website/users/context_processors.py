

def template_context_processor(request, *args, **kwargs):
    user = request.user
    return {'user': user}