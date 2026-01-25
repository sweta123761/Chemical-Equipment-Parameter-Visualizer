"""
Script to create the admin user for the application.
Run this if you're getting 401 Unauthorized errors.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user if it doesn't exist
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✅ User '{username}' already exists. Password has been reset to '{password}'.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ User '{username}' created successfully with password '{password}'.")

print("\nYou can now use these credentials:")
print(f"  Username: {username}")
print(f"  Password: {password}")
