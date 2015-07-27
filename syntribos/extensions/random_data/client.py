import uuid


def get_uuid():
    """Simple function for generating random data.
    Use for a unique value for each request when fuzzing.
    """
    while True:
        random_data = str(uuid.uuid4())
        yield random_data
