from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to  get a hashed password
def hash_password(password):
    return password_context.hash(password)