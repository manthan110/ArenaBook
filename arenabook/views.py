from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Turf, Booking, AppUser, Payment
from django.core.exceptions import ValidationError

def home(request):
    turfs = Turf.objects.all()
    return render(request, 'index.html', {'turfs': turfs})

def booking_page(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to book a turf.")
        return redirect('login')

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        time_format = '%H:%M'
        start_dt = datetime.strptime(start_time_str, time_format)
        end_dt = datetime.strptime(end_time_str, time_format)
        duration_hours = (end_dt - start_dt).total_seconds() / 3600
        total_amount = float(turf.price_per_hour) * duration_hours

        user = AppUser.objects.get(id=request.session['user_id'])

        Booking.objects.create(
            user=user,
            turf=turf,
            booking_date=booking_date,
            start_time=start_time_str,
            end_time=end_time_str,
            total_amount=total_amount,
            status='pending'
        )

        messages.success(request, f"Successfully booked {turf.turf_name} for ₹{total_amount}!")
        return redirect('home')

    return render(request, 'booking.html', {'turf': turf})

def login_page(request):
    error_message = None
    
    if request.method == 'POST':
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        
        user = AppUser.objects.filter(email=email_input, password=password_input).first()
        
        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            return redirect('home')
        else:
            error_message = "Invalid email or password."
            
    return render(request, 'login.html', {'error': error_message})

def logout_user(request):
    request.session.flush()
    return redirect('home')

def booking_page(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to book a turf.")
        return redirect('login')

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        time_format = '%H:%M'
        start_dt = datetime.strptime(start_time_str, time_format)
        end_dt = datetime.strptime(end_time_str, time_format)
        duration_hours = (end_dt - start_dt).total_seconds() / 3600
        total_amount = float(turf.price_per_hour) * duration_hours

        user = AppUser.objects.get(id=request.session['user_id'])

        try:
            new_booking = Booking(
                user=user,
                turf=turf,
                booking_date=booking_date,
                start_time=start_time_str,
                end_time=end_time_str,
                total_amount=total_amount,
                status='pending'
            )
            
            new_booking.full_clean() 
            new_booking.save()      

            return redirect('checkout_page', booking_id=new_booking.id)

        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)

    return render(request, 'booking.html', {'turf': turf})

def checkout_page(request, booking_id):
    if 'user_id' not in request.session:
        return redirect('login')
        
    booking = get_object_or_404(Booking, id=booking_id)
    user = AppUser.objects.get(id=request.session['user_id'])

    if booking.user != user:
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        Payment.objects.create(
            user=user,
            booking=booking,
            amount=booking.total_amount,
            payment_method=payment_method,
            status='completed'
        )
        
        booking.status = 'confirmed'
        booking.save()
        
        messages.success(request, f"Payment successful! Your reservation at {booking.turf.turf_name} is confirmed.")
        return redirect('home')

    return render(request, 'checkout.html', {'booking': booking})

def my_bookings(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to view your bookings.")
        return redirect('login')

    user_id = request.session['user_id']
    
    user_bookings = Booking.objects.filter(user_id=user_id).order_by('-created_at')

    return render(request, 'my_bookings.html', {'bookings': user_bookings})