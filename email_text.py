from theme import models, views

page = models.RegistrationPage.objects.all()[0]
u = models.CompanyProfile.objects.get(company="asdasd")

views.send_custom_email(page,u.user)
