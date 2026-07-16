from pydantic import BaseModel

class Feeds(BaseModel):
  feed_name: str
  weight: float
  feed_cost: float
  current_bags_stock: int

class ponds(BaseModel):
  pond_name: str
  pond_size: float
  pond_type: str
  pond_location: str
  pond_status: str

class Finance_cost(BaseModel):
  pond_id: int
  category: str
  description: str

class Finance_sales(BaseModel):
  stock_id: int
  quantity_sold: int
  total_weight: float
  price_sold_per_kg: float
  Total_sales: float

class Fish_stock(BaseModel):
  pond_id: str
  species: str
  initial_quantity: int
  current_quantity: int
  stocking_date: int
  Average_weight: float