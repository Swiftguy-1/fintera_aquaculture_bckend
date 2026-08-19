from pydantic import BaseModel
from datetime import date

class Feeds(BaseModel):
  feed_name: str
  weight: float
  feed_cost: float
  current_bags_stock: int

class ponds(BaseModel):
  pond_name: str
  pond_stock_quantity: float
  species_in_pond: str
  last_harvest_date: date
  pond_type: str
  pond_location: str
  pond_status: str
  water_temp: str
  pond_capacity: float

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

class mortality(BaseModel):
  Mortality_count: int 
  pond_name: str
  suspected_cause: str
  species: str

class harvest(BaseModel):
  pond_name: str
  species: str
  harvest_quantity: int
  total_weight: float
  harvest_date: date