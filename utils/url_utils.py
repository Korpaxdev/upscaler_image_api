from flask import url_for


def ex_url_for(endpoint: str, **kwargs):
    return url_for(endpoint, _external=True, **kwargs)
