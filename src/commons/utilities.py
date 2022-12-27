"""Utility tools for use throughout the project"""

def list_model_fields(Model):
    """Returns a list of the fields in a model"""
    fields = Model._meta.get_fields()
    return [field.name for field in fields]

def trim_dict(d, stencil):
    """
    Trim down the items of a dict to ensure only keys within the stencil are kept.

    Parameters:
    -------
    d: dict
        The dictionary to be trimmed.
    stencil: list
        The list of keys to kept, while anything not in this list is dropped.
    """
    trimmed_d = {}
    for k in d.keys():
        if k in stencil:
            trimmed_d[k] = d[k]
    return trimmed_d