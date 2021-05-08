
from django.http.response import HttpResponse
import smtplib
from .schema import *
from .utils import *

# Create your views here.
def hello(request):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("dheerukreddy@gmail.com", "Kmunna@!22001")

    # message to be sent
    message = "Message_you_need_to_send"

    # sending the mail
    s.sendmail("dheerukreddy@gmail.com", "dheerukreddy@gmail.com", message)

    # terminating the session
    s.quit()


    return HttpResponse('hdddd') 