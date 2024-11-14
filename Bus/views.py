from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .models import Bus,Location,Seat,Booking,Profile
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required,user_passes_test
from reportlab.pdfgen import canvas

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
         messages.success(request, ' Logout and try again')
         return redirect('/')

        
    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
            
        
    else:
        form = CreateUserForm()
        return render(request, "signup.html",{'form':form})
    

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='bus_operator').exists():
                return redirect('busopnavbar')
            else:
                return redirect('/')
        else:
            messages.success(request, 'wrong details.')
            
            return redirect('login')
            
        
    else:
        return render(request, 'login.html')
    
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    messages.success(request, 'u r logged out.')
    return redirect('/')

@login_required(login_url='/login') 
def index(request):
    return render(request,'home.html')

@login_required(login_url='/login')    
def search(request):
    
    
    item=Location.objects.all()
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r)
        if bus_list:
            return render(request,'buslist.html',{'buses': bus_list}) 
        else:
            messages.success(request, 'No bus available')
    return render(request,'findbus.html',{'item': item})

@login_required(login_url='/login') 
def busseat(request):
    bid_r = request.GET.get('bus_id')
  
    bus = Bus.objects.get(pk=bid_r)
    seats = Seat.objects.filter(bus_id=bid_r)
    context = {'bus': bus,'seats': seats}
    if request.method == 'POST':
        if not request.POST.get('seatid'):
            messages.success(request, 'Select a seat')
            return render(request,'busseat.html',context)
        else :
            uid_r = request.user.id
            selected_seat = request.POST.get('seatid').split(':')
            seatid_r = selected_seat[0]
            seatno_r = selected_seat[1]
            price_r = request.POST.get('price')
            departure_date_r = request.POST.get('departure_date')
            Seat.objects.filter(id=seatid_r).update(is_available=False)
            Booking.objects.create(user_id=uid_r,bus_id=bid_r,seatno=seatno_r,price=price_r,departure_date=departure_date_r)
            messages.success(request, 'Booked successfully')
            return redirect('/')
    else:

        return render(request,'busseat.html',context)

@login_required(login_url='/login') 
def reservation(request):
    items = Booking.objects.filter(user_id=request.user.id)
    if items:
        context={'items': items}
        return render(request,'reservation.html',context)
    else:
        messages.success(request, 'No prior reservationsss')
        return redirect('/search')


from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from io import BytesIO
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

def generate_pdf(request):
    id = request.GET.get('id')
    # Fetch the booking data from the database
    booking = Booking.objects.get(pk=id)
    busop = Profile.objects.get(user_id=booking.bus.bus_operator_id)

    # Split the contact information into separate lines
    contact_lines = busop.contact.split('\n')

    # Create a new PDF object
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Set up the ticket layout
    
    pdf.setFillColorRGB(0.95, 0.95, 0.95)
    pdf.roundRect(1 * cm, 1 * cm, 28 * cm, 14 * cm, 10, fill=1)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.roundRect(1 * cm, 1 * cm, 28 * cm, 14 * cm, 10)

    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(15 * cm, 13 * cm, 'BUS TICKET')

    pdf.setFont('Helvetica', 14)
    pdf.drawString(2 * cm, 9.5 * cm, f'Passenger Name: {request.user.first_name} {request.user.last_name}')
    pdf.drawString(2 * cm, 8.5 * cm, f'Bus Name: {booking.bus.bname}')
    pdf.drawString(2 * cm, 7.5 * cm, f'From: {booking.bus.source}')
    pdf.drawString(2 * cm, 6.5 * cm, f'To: {booking.bus.dest}')
    pdf.drawString(2 * cm, 5.5 * cm, f'Departure Date: {booking.departure_date.strftime("%d-%m-%Y")}')
    pdf.drawString(2 * cm, 4.5 * cm, f'Seat No: {booking.seatno}')

    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawCentredString(15 * cm, 9 * cm, 'BUS OPERATOR DETAILS')

    pdf.setFont('Helvetica', 14)
    y_pos = 8 * cm
    for line in contact_lines:
        pdf.drawString(12 * cm, y_pos, f'{line}')
        y_pos -= 0.7 * cm

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawRightString(27 * cm, 1.5 * cm, f'Total Price: {booking.price}')

    pdf.showPage()
    pdf.save()

    # Set the buffer's position to its beginning
    buffer.seek(0)

    # Return the PDF as a response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bus_ticket.pdf"'
    return response


@login_required(login_url='/login')    
def busopnavbar(request):
    if request.user.groups.filter(name='bus_operator').exists():
        
        return render(request,'busopnavbar.html')
    else:
        return redirect('/')


@user_passes_test(lambda u: u.groups.filter(name='bus_operator').exists(), login_url='/')
def busopbus(request):
    if request.user.groups.filter(name='bus_operator').exists():
        bus_list = Bus.objects.filter(bus_operator_id=request.user.id)
        if bus_list:
            return render(request,'busopbus.html',{'buses': bus_list}) 
        else:
            messages.success(request, 'No bus available')
            return render(request,'busopbus.html',{'buses': bus_list})
    else:
        return redirect('/')
    


    
@login_required(login_url='/login')    
def busopbooking(request):
    if request.user.groups.filter(name='bus_operator').exists():
        bookings=Booking.objects.filter(bus__bus_operator_id=request.user.id).order_by('bus_id')
        context={'bookings': bookings}        


        return render(request,'busopbooking.html',context)
    else:
        return redirect('/')
    



    

    
    

