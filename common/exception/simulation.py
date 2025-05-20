class WeaponMissingError(Exception):
    """Exception raised when a weapon is missing."""
    def __init__(self, message="Weapon is missing."):
        self.message = message
        super().__init__(self.message)