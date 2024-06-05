from enum import Enum

class Role(str, Enum):
    admin = "Admin"
    user = "User"
    waiter = "Waiter"