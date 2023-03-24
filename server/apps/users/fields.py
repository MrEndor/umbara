from server.apps.core import fields
from server.apps.users.models import Profile, UserWithProfile

EmailFieldUser: str = fields.get_field_name(UserWithProfile.email)
UserNameFieldUser: str = fields.get_field_name(UserWithProfile.username)
FirstNameFieldUser: str = fields.get_field_name(UserWithProfile.first_name)
LastNameFieldUser: str = fields.get_field_name(UserWithProfile.last_name)

BirthdayFieldProfile: str = fields.get_field_name(Profile.birthday)
CoffeeCountFieldProfile: str = fields.get_field_name(Profile.coffee_count)
ImageFieldProfile: str = fields.get_field_name(Profile.image)
