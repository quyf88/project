from django.shortcuts import render

# Create your views here.
li = ['q', 'w', 'e', 'r']
tu = ('a', 's', 'd', 'f')
dic = {'x': 1, 'y': 2}
st = 'this is django course'


def index(request):
    """
    模板传值
    :param request:
    :return:
    """
    return render(request, 'test_index.html',
                  context={
                            'li': li,
                           'tu': tu,
                           'dic': dic,
                           'str': st,
                            'name': 'dandan',
                            'li1': [1,2,3,4,5,6,7,8,9],
                            'li2': [1,2,3,4,5,6,7,8,9],
                  })