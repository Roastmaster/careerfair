from theme. views import get_bill, update_rep_data
from theme.models import CompanyProfile

for comp in CompanyProfile.objects.all():
    print comp.sponsor
    comp.total_bill = get_bill(comp)[2]
    update_rep_data(comp)
    comp.save()
    print comp.total_bill
