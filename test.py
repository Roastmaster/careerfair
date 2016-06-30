from theme import models
from theme import views

page = models.RegistrationPage.objects.all()[0]
comp = models.CompanyProfile.objects.get(company="Fake Company")

print comp.user.companyprofile
views.send_custom_email(page, comp.user)

