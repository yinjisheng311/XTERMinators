from django.shortcuts import render

# Create your views here.
def home_view(request):
	template_name='home.html'
	return render(request,template_name)

def host_view(request,host_name):
	template_name='host.html'
	context={'host':host_name}
	return render(request,template_name,context)