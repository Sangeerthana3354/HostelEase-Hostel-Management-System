from django.shortcuts import render, redirect,get_object_or_404
from Studentapp.models import Complaintdb
from Hostelapp.models import Roomdb, Messdb, Studentdb,Payment
import razorpay
from django.conf import settings


# Create your views here.
def home_page(request):
    if not request.session.get('student_id'):
        return redirect('student_login_page')

    return render(request, "Home.html")

def room_page(request):
    rooms = Roomdb.objects.all()
    for room in rooms:
        if room.Capacity and room.Capacity > 0:
            room.percent = int((room.Occupied / room.Capacity) * 100)
            if room.Occupied >= room.Capacity:
                room.percent = 100
        else:
            room.percent = 0
        if room.Rent_price:
            room.monthly_rent = int(room.Rent_price / 12)
        else:
            room.monthly_rent = 0
    return render(request, "Room.html", {"rooms": rooms})
def mess_page(request):
    mess = Messdb.objects.last()
    weekly = Messdb.objects.all()
    return render(request, "Menu.html", {"mess": mess, "weekly": weekly})
def gallery_page(request):
    return render(request, "Gallery.html")
def student_complaint(request):
    return render(request, "Complaint.html")
def save_complaint(request):
    if request.method == "POST":
        student_name = request.POST.get("name")
        room_no = request.POST.get("room")
        complaint_type = request.POST.get("category")
        description = request.POST.get("message")
        Complaintdb.objects.create(
            Student_name=student_name,
            Room_no=room_no,
            Complaint_type=complaint_type,
            Description=description
        )
        return redirect('student_complaint_success')
def student_complaint_success(request):
    return render(request, "Complaint_success.html")
def student_profile(request):
    sid = request.session.get("student_id")
    if not sid:
        return redirect("student_login_page")  # redirect to login page
    student = Studentdb.objects.get(id=sid)
    room_count = Roomdb.objects.count()
    complaint_count = Complaintdb.objects.filter(Student_name=student.Name).count()
    context = {
        "student": student,
        "room_count": room_count,
        "complaint_count": complaint_count,
        "payment_count": 0,  # will connect later
        "visitor_count": 0,  # will connect later
    }
    return render(request, "Profile.html", context)
def edit_student_profile(request, sid):
    student = Studentdb.objects.get(id=sid)
    return render(request, 'Edit_Profile.html', {'student': student})
def update_student_profile(request, sid):
    if request.method == "POST":
        Studentdb.objects.filter(id=sid).update(
            Name=request.POST.get('name'),
            Age=request.POST.get('age'),
            Gender=request.POST.get('gender'),
            Room=request.POST.get('room'),
            Phone=request.POST.get('phone'),
            Parent_phone=request.POST.get('parent'),
            Address=request.POST.get('address'),
        )
        return redirect('student_profile')
def student_login_page(request):
    return render(request, "Student_login.html")
def student_login(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")

        student = Studentdb.objects.filter(
            Username__iexact=uname.strip(),
            Password=pwd.strip()
        ).first()

        if student:
            request.session['student_id'] = student.id
            return redirect('home_page')

        return render(request, "Student_Login.html", {
            "msg": "Invalid username or password"
        })

    return render(request, "Student_Login.html")


def student_profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')
    student = Studentdb.objects.get(id=student_id)
    return render(request, 'Profile.html', {'student': student})
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)
def student_payments(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")
    student = get_object_or_404(Studentdb, id=student_id)
    payments = Payment.objects.filter(student=student)
    for payment in payments:
        if payment.status == "Pending" and not payment.razorpay_order_id:
            order = client.order.create({
                "amount": payment.amount * 100,  # paise
                "currency": "INR",
                "payment_capture": 1
            })
            payment.razorpay_order_id = order["id"]
            payment.save()
    return render(request, "payments.html", {
        "payments": payments,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })
def payment_success(request):
    pid = request.GET.get("pid")
    razorpay_payment_id = request.GET.get("razorpay_payment_id")

    payment = get_object_or_404(Payment, id=pid)
    payment.status = "Paid"
    payment.razorpay_payment_id = razorpay_payment_id
    payment.save()

    return render(request, "payment_success.html")

