
def custom_proc(request):

    return {
        'is_authenticated': request.user.is_authenticated,
    }
