from pydantic import BaseModel, Field

class TextBlock(BaseModel):
    text : str
    x : float # with x: float, if someone passes x="five", Pydantic raises a ValidationError immediately — same tripwire as confidence. With coords: tuple, that same string still slides past silently
    y : float
    width: float
    height: float
    page_number : int
    confidence : float = Field(ge=0.0, le=1.0)