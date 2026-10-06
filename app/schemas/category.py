from pydantic import BaseModel, ConfigDict


# Какие данные API принимает и отдаёт?
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str