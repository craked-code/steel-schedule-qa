from pydantic import BaseModel, Field
from typing import Optional, Literal

class TextBlock(BaseModel):
    text : str
    x : float # with x: float, if someone passes x="five", Pydantic raises a ValidationError immediately — same tripwire as confidence. With coords: tuple, that same string still slides past silently
    y : float
    width: float
    height: float
    page_number : int
    confidence : float = Field(ge=0.0, le=1.0)

class TableCell(BaseModel):
    text : str
    row_num : int
    col_num : int

class ScheduleRow(BaseModel):
    mark : str
    section_designation : str = 'UNREADABLE'
    material : Optional[str] = None
    notes : Optional[str] = None

class SteelSection(BaseModel):
    type : str
    designation : str
    depth : float
    weight_or_thickness : Optional[float] = None
    width : Optional[float] = None

class QAResult(BaseModel):
    mark : str
    designation : str
    status : Literal['PASS', 'WARNING: NOT FOUND', 'ERROR: INVALID DESIGNATION', 'INFO: DUPLICATE']
    message : str
    section_properties : Optional[dict] = None

class AnalysisResponse(BaseModel):
    filename : str
    pages_processed : int
    schedule_rows : list[ScheduleRow]
    qa_results : list[QAResult]
    summary : dict