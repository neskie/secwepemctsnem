def variables(request):
    """
    Returns the variables in the arg 
    """
    s = request.GET.get('secwepemc')
    e = request.GET.get('english')
    return {'secwepemc': s, 'english': e}
