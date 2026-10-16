from pydantic import BaseModel, Field, field_validator, ValidationError

class AskRequest(BaseModel):
    query: str = Field(min_length=1,  )

    @field_validator('query')
    @classmethod
    def clean_and_check_empty(cls, v: str) -> str:
        # 1. Strip leading and trailing whitespace
        cleaned = v.strip()
        
        # 2. Check if the string is empty after stripping
        if not cleaned:
            raise ValueError("query cannot be empty or just whitespace")
        
        # 3. Return the transformed value so Pydantic uses it
        return cleaned

class SourceItem(BaseModel):

    source_id: str 
    chunk_id : str 
    source_path : str 
    page_number: int 
    similarity : float
    
class AskResponse(BaseModel):

    answer: str 
    sources: list[SourceItem] = Field(default_factory=list)
