# users/utils.py

def is_admin(user):
    """
    Check if user is Admin
    """
    return user.is_authenticated and user.is_staff


def is_analyst(user):
    """
    Check if user is Analyst (read-only user)
    """
    return user.is_authenticated and not user.is_staff
