"""
This class helps returning API response consistent
with DRF Response structure
"""

class APIResponse:
    
    def __init__(self, **kwargs) -> None:
        for k,v in kwargs.items():
            self.__dict__[k] = v
    