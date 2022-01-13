from django.shortcuts import render

# Create your views here.
def view_home_page(request):
    return render(request, 'pages/home.html')


def view_contact_page(request):
    return render(request, 'pages/contact.html')