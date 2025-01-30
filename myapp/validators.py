import re
from django.core.exceptions import ValidationError

# EX Validation for uppercase
class UppercaseValidator(object):
    def validate(self, password1, user=None):
        if not re.findall('[A-Z]', password1):
            raise ValidationError(
                ("The password must contain at least 1 uppercase letter, A-Z.")
            )
    
    def get_help_text(self):
        return("your password must contain one upper case letter.")