from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str
    password: str

    # role = Column(Enum(Role), default=Role.user)