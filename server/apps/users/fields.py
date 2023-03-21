from server.apps.core import fields
from server.apps.users.models import Profile, User

EmailFieldUser: str = fields.get_field_name(User.email)
UserNameFieldUser: str = fields.get_field_name(User.username)
FirstNameFieldUser: str = fields.get_field_name(User.first_name)
LastNameFieldUser: str = fields.get_field_name(User.last_name)

BirthdayFieldProfile: str = fields.get_field_name(Profile.birthday)
CoffeeCountFieldProfile: str = fields.get_field_name(Profile.coffee_count)
ImageFieldProfile: str = fields.get_field_name(Profile.image)
