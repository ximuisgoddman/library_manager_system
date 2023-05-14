def user(request):
    print("@@@@",request.user,dir(request.user))
    return {'user': request.user}
