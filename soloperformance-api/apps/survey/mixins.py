




class CreateAnswerListMixin:
    """Allows bulk creation of a resource."""
    def get_serializer(self, *args, **kwargs):
        print(isinstance(kwargs.get('data', {}), list))
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)