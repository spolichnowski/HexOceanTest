def validate_extension(value):
    '''Validation accepts only JPEG and PNG formats.'''
    from django.core.exceptions import ValidationError
    import os
    extension = os.path.splitext(value.name)[1]
    if extension.lower() not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError(
            'Image extension is not valid. Try again with JPG or PNG format.')
