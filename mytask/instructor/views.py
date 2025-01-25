from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import random
import json
import re
from django.core.mail import send_mail
import logging
import string

client = MongoClient('mongodb://localhost:27017/')
db = client['mytask']
instructor_collection = db["instructor"]

def generate_otp():
    return random.randint(100000, 999999)
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def send_email(to_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message="",
            html_message=message,
            from_email='mugil1206@gmail.com',
            recipient_list=[to_email],
        )
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
logger=logging.getLogger(__name__)

@csrf_exempt
def register_instructor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            
            if not all([first_name, last_name, email, password, confirm_password]):
                return JsonResponse({'error': 'Please fill all fields'}, status=400)
            if not is_valid_email(email):
                return JsonResponse({'error': 'Invalid email'}, status=400)
            if len(password) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
            
            if instructor_collection.find_one({'email': email}):
                return JsonResponse({'error': 'Email already exists'}, status=400)
            email_otp = generate_otp()
            email_message = f"<p>Your OTP is: <strong>{email_otp}</strong></p>"
            email_sent = send_email(email, "email verification otp", email_message)
            if not email_sent:
                return JsonResponse({'error': 'Failed to send email'}, status=400)
            instructor_collection.insert_one({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "email_verified": False,
                "email_otp": email_otp,
            })
            return JsonResponse({'message': 'Instructor registered successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"unexpected error: {str(e)}")
            return JsonResponse({'error': 'Unexpected error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def verify_email_otp(request)
            
                
                