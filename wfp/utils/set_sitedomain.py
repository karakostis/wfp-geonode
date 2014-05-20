from django.contrib.sites.models import Site
s = Site.objects.all()[0]
s.domain = 'localhost:8000'
s.save()
