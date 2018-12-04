import uuid


def g_uid():
    x = uuid.uuid4()
    print(str(x))
    return str(x)

g_uid()