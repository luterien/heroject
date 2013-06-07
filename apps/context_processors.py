from apps.profiles.models import Profile

def custom_context(request):

	p = Profile.objects.from_request(request)

	return {'profile':p}