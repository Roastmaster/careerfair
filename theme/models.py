from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.utils.encoding import python_2_unicode_compatible
from mezzanine.conf import settings
from django import forms 
import django

from django.utils.translation import ugettext_lazy as _
import uuid

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.forms.models import Form
from mezzanine.forms import fields
from mezzanine.utils.models import upload_to
from multiselectfield import MultiSelectField
from customutils import ContentTypeRestrictedFileField
#
#
# REGISTRATION FORMS:

VOLUNTEER_CHOICES = (('Armory', 'Armory'),
                    ('Food', 'Food'),
                    ('Something else', 'Something else'))

DAY_CHOICES = (('Friday', 'Friday'),
                ('Saturday', 'Saturday'))

MAJOR_CHOICES = (('Aeronautical Engineering', 'Aeronautical Engineering'),
                ('Applied Physics', 'Applied Physics'),
                ('Architecture', 'Architecture'),
                ('Biochemistry and Biophysics', 'Biochemistry and Biophysics'),
                ('Bioinformatics and Molecular Biology', 'Bioinformatics and Molecular Biology'),
                ('Biology', 'Biology'),
                ('Biomedical Engineering', 'Biomedical Engineering'),
                ('Building Science', 'Building Science'),
                ('Business and Management', 'Business and Management'),
                ('Chemical Engineering', 'Chemical Engineering'),
                ('Chemistry', 'Chemistry'),
                ('Civil Engineering', 'Civil Engineering'),
                ('Cognitive Science', 'Cognitive Science'),
                ('Communication', 'Communication'),
                ('Computer and Systems Engineering', 'Computer and Systems Engineering'),
                ('Computer Science', 'Computer Science'),
                ('Design, Innovation, and Society', 'Design, Innovation, and Society'),
                ('Economics', 'Economics'),
                ('Electrical Engineering', 'Electrical Engineering'),
                ('Electronic Arts', 'Electronic Arts'),
                ('Electronic Media, Arts, and Communication', 'Electronic Media, Arts, and Communication'),
                ('Environmental Engineering', 'Environmental Engineering'),
                ('Environmental Science', 'Environmental Science'),
                ('Games and Simulation Arts and Sciences', 'Games and Simulation Arts and Sciences'),
                ('Geology', 'Geology'),
                ('Hydrogeology', 'Hydrogeology'),
                ('Industrial and Management Engineering', 'Industrial and Management Engineering'),
                ('Information Technology and Web Science', 'Information Technology and Web Science'),
                ('Interdisciplinary Science', 'Interdisciplinary Science'),
                ('Materials Engineering', 'Materials Engineering'),
                ('Mathematics', 'Mathematics'),
                ('Mechanical Engineering', 'Mechanical Engineering'),
                ('Nuclear Engineering', 'Nuclear Engineering'),
                ('Philosophy', 'Philosophy'),
                ('Physics', 'Physics'),
                ('Psychology', 'Psychology'),
                ('Science, Technology, and Society', 'Science, Technology, and Society'),
                ('Sustainability Studies', 'Sustainability Studies'))

MINOR_CHOICES = (('------------','-----------'),
                    ('Acoustics', 'Acoustics'),
                    ('Air and Space Leadership Studies', 'Air and Space Leadership Studies'),
                    ('Architecture', 'Architecture'),
                    ('Astrobiology', 'Astrobiology'),
                    ('Astronomy', 'Astronomy'),
                    ('Astrophysics', 'Astrophysics'),
                    ('Biochemistry', 'Biochemistry'),
                    ('Biology', 'Biology'),
                    ('Biophysics', 'Biophysics'),
                    ('Brain and Brain Behavior', 'Brain and Brain Behavior'),
                    ('Chemistry', 'Chemistry'),
                    ('Civil Engineering', 'Civil Engineering'),
                    ('Chinese', 'Chinese'),
                    ('Cognition', 'Cognition'),
                    ('Communication', 'Communication'),
                    ('Community and Health Psychology', 'Community and Health Psychology'),
                    ('Computer Science', 'Computer Science'),
                    ('Computer and Systems Engineering', 'Computer and Systems Engineering'),
                    ('Electrical Power Engineering', 'Electrical Power Engineering'),
                    ('Electrical Engineering', 'Electrical Engineering'),
                    ('Electronic Arts', 'Electronic Arts'),
                    ('Electronic Media, Arts, and Communication', 'Electronic Media, Arts, and Communication'),
                    ('Energy', 'Energy'),
                    ('Entrepreneurship', 'Entrepreneurship'),
                    ('Environmental Engineering', 'Environmental Engineering'),
                    ('Environmental Science', 'Environmental Science'),
                    ('Finance', 'Finance'),
                    ('Games and Simulation Arts and Sciences', 'Games and Simulation Arts and Sciences'),
                    ('Geology', 'Geology'),
                    ('Game Studies', 'Game Studies'),
                    ('Gender, Science and Technology', 'Gender, Science and Technology'),
                    ('History of Architecture', 'History of Architecture'),
                    ('Hydrogeology', 'Hydrogeology'),
                    ('Human-Computer Interaction', 'Human-Computer Interaction'),
                    ('Human Factors in Psychology', 'Human Factors in Psychology'),
                    ('Industrial/Organizational Psychology', 'Industrial/Organizational Psychology'),
                    ('Industrial and Management Engineering', 'Industrial and Management Engineering'),
                    ('Lighting', 'Lighting'),
                    ('Literature', 'Literature'),
                    ('Logic, Computation and Mind', 'Logic, Computation and Mind'),
                    ('Management', 'Management'),
                    ('Marketing', 'Marketing'),
                    ('Materials Engineering', 'Materials Engineering'),
                    ('Mathematics', 'Mathematics'),
                    ('Military Studies', 'Military Studies'),
                    ('Music', 'Music'),
                    ('Origins of Life', 'Origins of Life'),
                    ('Philosophy of Human Values and Society', 'Philosophy of Human Values and Society'),
                    ('Philosophy of Logic, Computation and Mind', 'Philosophy of Logic, Computation and Mind'),
                    ('Philosophy of Science and Technology', 'Philosophy of Science and Technology'),
                    ('Philosophy', 'Philosophy'),
                    ('Physics', 'Physics'),
                    ('Professional Writing', 'Professional Writing'),
                    ('Psychology', 'Psychology'),
                    ('Science, Technology, and Society', 'Science, Technology, and Society'),
                    ('Social Psychology', 'Social Psychology'),
                    ('Sports Psychology', 'Sports Psychology'),
                    ('Sustainability Studies', 'Sustainability Studies'),
                    ('Studio Arts', 'Studio Arts'),
                    ('Technology Commercialization and Entrepreneurship', 'Technology Commercialization and Entrepreneurship'),
                    )

GRADE_LEVEL_CHOICES = (('Freshman', 'Freshman'),
                       ('Sophomore', 'Sophomore'),
                       ('Junior', 'Junior'),
                       ('Senior', 'Senior'),
                       ('Graduate', 'Graduate'),
                       ('PhD', 'PhD'))

MAJOR_CHOICES_FLAT = [major[0] for major in MAJOR_CHOICES]

#
#
# SPONSORSHIP PAGE:
#

class SponsorUsPage(Page, RichText):
    super_heading = models.CharField(max_length=100)
    blurb = RichTextField(max_length=3000, help_text="Some paragraph of text above the segment of the page where the sponsorship packages are listed")
    contact = RichTextField(max_length=1000)

class SponsorshipPackage(models.Model):
    level = models.IntegerField(help_text="This is the ranking of this package. Each Sponsorship package should be ranked from worst to best.  1 is worst, highest is best.")
    title = models.CharField(help_text="What do you name this package? This will appear on the sponsorus page", max_length=100)
    description = RichTextField(help_text="In detail, describe the amenities of the package.  Be sure to format it nicely because whatever you write here will be displayed on the sponsor us page.")
    price = models.IntegerField(help_text="Finally, put the price.")
    sponsoruspage = models.ForeignKey(SponsorUsPage, related_name="sponsorship_package")

    def __unicode__ (self):
        return self.title

#
#
# Student profile
#

from .validators import validate_file_extension
class StudentProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(blank=True, max_length=14)
    grade_level = MultiSelectField(choices=GRADE_LEVEL_CHOICES, max_choices=1, blank=True)
    major = MultiSelectField(choices=MAJOR_CHOICES, max_choices=2, blank=True)
    minor = MultiSelectField(choices=MAJOR_CHOICES, max_choices=1, blank=True)
    resume = models.FileField(upload_to='resumes', blank=True)
    picture = models.ImageField(upload_to='uploads/student_images', blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    open_to_relocation = models.BooleanField(default=False, blank=True, help_text="Open to relocation?")
    GPA = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    website = models.CharField(max_length=500, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.last_name + ", " + self.first_name

    class Meta:
        get_latest_by = 'creation_date'

class StudentSearchFormModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    grade_level_wanted = MultiSelectField(choices=GRADE_LEVEL_CHOICES, blank=True)
    major_wanted = MultiSelectField(choices=MAJOR_CHOICES, blank=True)
    open_to_relocation = models.BooleanField(default=False, blank=True)
    minimum_GPA = models.DecimalField(max_digits=3, decimal_places=2, null=True)


#
#
# Company profile

class CompanyRep(models.Model):
    rep = models.CharField(max_length=100)
    is_alumni = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.rep


from django.db.models.signals import pre_delete 
from django.dispatch import receiver



#
#
# REGISTRATION PAGE:

class RegistrationPage(Page, RichText):

    button_text = models.CharField(_("Button text"), max_length=50, blank=True)
    response = RichTextField(_("Response"))
    send_email = models.BooleanField(_("Send email to user"), default=True,
        help_text=_("To send an email to the email address supplied in "
                    "the form upon submission, check this box."))
    email_from = models.EmailField(_("From address"), max_length=254,
        help_text=_("The address the email will be sent from"), blank=True)
    email_subject = models.CharField(_("Subject"), max_length=200, blank=True)
    email_message = models.TextField(_("Message"), blank=True,
        help_text=_("Emails sent based on the above options will contain "
                    "each of the form fields entered. You can also enter "
                    "a message here that will be included in the email."))
    email_copies = models.CharField(_("Send email to others"), blank=True,
        help_text=_("Provide a comma separated list of email addresses "
                    "to be notified upon form submission. Leave blank to "
                    "disable notifications."),
        max_length=200)
    google_maps_api_key = models.CharField(max_length=200, blank=True, 
        help_text="Google how to obtain a google maps key for the location mueller center and past it here")
    text_under_map = models.TextField(max_length=1000, blank=True)
    class Meta:
        verbose_name = _("Registration Page")
        verbose_name_plural = _("Registration Pages")

#
# ABOUT PAGE:
#

class AboutPage(Page, RichText):
    super_heading = models.CharField(max_length= 100)
    heading1 = models.CharField(max_length= 50,
        help_text="Header for column 1")
    heading2 = models.CharField(max_length= 50,
        help_text="Header for column 2")
    heading3 = models.CharField(max_length= 50,
        help_text="Header for column 3")
    LeftColumn = RichTextField(max_length= 3000,
        help_text="Blurb under heading1",
        default="")
    MidColumn = RichTextField(max_length= 3000,
        help_text="Blurb under heading2",
        default="")
    RightColumn = RichTextField(max_length= 3000,
        help_text="Blurb under heading3",
        default="")
    heading4 = models.CharField(max_length= 50,
        help_text="Header for bottom blurb",
        default= "Our Team")
    BottomRow = RichTextField(max_length=3000,
        help_text="Blurb under heading4",
        default="")


class StaffProfile(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    aboutpage = models.ForeignKey(AboutPage, related_name="staff_profile")
    name = models.CharField(max_length = 100, help_text="Enter the name of the staff memeber here")
    position = models.CharField(max_length = 100, help_text="Enter their position among the career fair staff")
    bio = RichTextField(max_length = 1000, help_text="Enter a short bio of that person and their duties")
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.Slide.image", "Headshots"),
        format="Image", max_length=255, null=True, blank=True)
#
#
# AGENDA PAGE:
#

class AgendaPage(Page, RichText):
    heading = models.CharField(max_length=200,
        help_text="Put title here or something")
    friday = RichTextField(max_length=30000, help_text="Enter a nicely formatted schedule of friday here")
    saturday = RichTextField(max_length=30000, help_text="Enter a nicely formatted schedule of saturday here")

#
#
# CONTACT PAGE:
#

class ContactPage(Page, RichText):
    heading = models.CharField(max_length=200,
        help_text="Put title here or something")
    contact_info = RichTextField(max_length=30000, help_text="Enter a nicely formatted contact page here")

class PricingPage(Page, RichText):
    heading = models.CharField(max_length=200,
        help_text="Put title here or something")
    pricing_info = RichTextField(max_length=30000, help_text="Enter a nicely formatted pricing page here, complete with any sponsorship information you could think of.")

#
#
# HOMEPAGE:
#

class HomePage(Page, RichText):
    '''
    A page representing the format of the home page
    '''
    heading = models.CharField(max_length=200,
        help_text="Put title here or something")
    hptime = models.CharField(max_length=200,
        help_text="Time, Data, Location",
        default= "00:00:00")
    hpdate = models.CharField(max_length=200,
        help_text="Date",
        default= "00/00/00")
    hploc = models.CharField(max_length=200,
        help_text="Location",
        default="Aaa, Aaa")
    subheading = RichTextField(max_length=1000,
        help_text="Some text explaining what the career fair is",
        default= "Write something here already")
    IconText1 = models.CharField(max_length = 200,
        default = "IconText1", blank=True)
    IconTitle1 = models.CharField(max_length = 50,
        default = "IconTitle1", blank=True)
    IconText2 = models.CharField(max_length = 200,
        default = "IconText2", blank=True)
    IconTitle2 = models.CharField(max_length = 50,
        default = "IconTitle2", blank=True)
    IconText3 = models.CharField(max_length = 200,
        default = "IconText3", blank=True)
    IconTitle3 = models.CharField(max_length = 50,
        default = "IconTitle3", blank=True)
    IconText4 = models.CharField(max_length = 200,
        default = "IconText4", blank=True)
    IconTitle4 = models.CharField(max_length = 50,
        default = "IconTitle4", blank=True)
    IconUrl1 = models.CharField(max_length = 1000,
        default = "#")
    IconUrl2 = models.CharField(max_length = 1000,
        default = "#")
    IconUrl3 = models.CharField(max_length = 1000,
        default = "#")
    IconUrl4 = models.CharField(max_length = 1000,
        default = "#")
    featured_companies_heading = models.CharField(max_length=200,
        default = "Featured Companies")
    announcement_header = models.CharField(max_length = 30,
        help_text = "Title for announcements field",
        default = "Announcements")
    content_heading = models.CharField(max_length=200,
        default="About us!")
    latest_posts_heading = models.CharField(max_length=200,
        default="Latest Posts")
    misc_info_header = models.CharField(max_length = 30,
        help_text = "Title for misc info field",
        default = "About us")
    misc_info_body = RichTextField(max_length = 2000,
        help_text = "Body for misc info field",
        default = "About us")

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

class FAQPage(Page, RichText):
    heading = models.CharField(max_length=200,
        help_text="Put title here or something")


class Question(Orderable):
    faqpage = models.ForeignKey(FAQPage, related_name="question")
    question = RichTextField(_("Question"))
    answer = RichTextField(_("Answer"))

class ArmoryTableData(models.Model):
    friday_reservations = models.TextField(null=True)
    saturday_reservations = models.TextField(null=True)

class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.Slide.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)


class FeaturedCompany(Orderable):
    '''
    A showcase of featured company logos connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="featured_companies")
    image = FileField(verbose_name=_("Image"),
        help_text="A square, transparent image (or white background) to represent the company on the frontpage slider.  Make sure it's a square.",
        upload_to=upload_to("theme.FeaturedCompany.image", "Featured Companies"),
        format="Image", max_length=255, null=True, blank=True)
    link_to = models.CharField(max_length = 1000,
        help_text = "A link to the company's application site",
        default = "http://")



class Announcement(Orderable):
    '''
    A slide of all the latest announcements posted by site admin
    '''
    homepage = models.ForeignKey(HomePage, related_name="announcements")
    date = models.CharField(max_length = 6,
        help_text = "Date (no year) DD MMM ",
        default = "01 Jan")
    year = models.CharField(max_length = 5,
        help_text = "Year YYYY",
        default = "0000")
    announcement_title = models.CharField(max_length = 100,
        help_text = "Title of your announcement post",
        default = "Announcement here!")
    announcement_text = models.TextField(max_length = 500,
        help_text = "Type your new announcement here",
        default = "")
    author = models.CharField(max_length = 100,
        help_text = "Type your name as you want it to appear",
        default = "")


class IconBlurb(Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="blurbs")
    icon = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.IconBlurb.icon", "icons"),
        format="Image", max_length=255)
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.CharField(max_length=2000, blank=True,
        help_text="Optional, if provided clicking the blurb will go here.")



# This is the class that allows people to edit the price and account names and what not
# from the front end
class PayPalInfo(models.Model):
    email = models.EmailField(default="", help_text="The email account associated with whatever paypal account you plan on using")
    friday_price = models.IntegerField(help_text="Friday's price", default = 500)
    saturday_price = models.IntegerField(help_text="Saturday's price", default = 500)
    price_per_rep = models.IntegerField(help_text="Price per representative", default = 75)
    price_per_alumni_rep = models.IntegerField(help_text="Price per RPI alumni representative", default=0)
    price_per_table = models.IntegerField(help_text="Price per table", default=100)
    sponsorship = models.IntegerField(help_text="How much do you want to charge for sponsorships?", default=0)
    item_name = models.CharField(help_text="What is the name of the item/service they are buying?",
        max_length=400, 
        default="SHPE Company Career Fair Registration Fee 2016")
    class Meta:
        verbose_name = _("PayPal Info")
        verbose_name_plural = _("PayPal Info")

    def __unicode__(self):
        return self.email

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "roastmiester@gmail.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        user_id = ipn_obj.custom
        company = User.objects.get(id=user_id).companyprofile
        company.has_submitted_payment = True
        company.save()
        print "my boy got saved", User.objects.get(id=user_id).companyprofile.has_submitted_payment
    else:
        print "uh oh send an email"
        print ipn_obj.payment_status
        #...

valid_ipn_received.connect(show_me_the_money)