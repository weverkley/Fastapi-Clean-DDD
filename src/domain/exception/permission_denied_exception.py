class PermissionDeniedException(Exception):
    """
    Custom exception raised when a user lacks permission to access a resource.

    Attributes:
        message -- explanation of the error
        resource -- the resource that was being accessed (optional)
        user_id -- the ID of the user who was denied (optional)
    """
    def __init__(self, message="User does not have permission to access this resource.", resource=None, user_id=None):
        self.resource = resource
        self.user_id = user_id
        # You can format a more detailed message if extra info is provided
        if resource and user_id:
            self.message = f"User '{user_id}' denied access to resource '{resource}'."
        elif resource:
            self.message = f"Permission denied for resource: '{resource}'."
        else:
            self.message = message
        
        super().__init__(self.message)

    def __str__(self):
        return f'[PermissionDeniedException]: {self.message}'