

def get_or_none(cls, *args, **kwargs):
    try:
        return cls._default_manager.get(*args, **kwargs)
    except cls.DoesNotExist:
		return None

