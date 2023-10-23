import random
import string

def generate_unique_pid():
    """Generate a unique profile id for the user consisting of random characters.
    """
    length = 16
    pattern = string.digits+string.ascii_lowercase+string.ascii_uppercase
    while True:
        code = ''.join(random.choices(pattern, k=length))
        return code