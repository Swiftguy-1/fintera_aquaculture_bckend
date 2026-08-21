from pydantic import BaseModel
from datetime import date

class Feed_inventory(BaseModel):
  feed_name: str
  feed_type: str
  quantity: int
  av_weight_per_bag: float
  feed_cost_per_bag: float
  feed_total_cost: float
  supplier: str
  expiry_date: date
  purchase_date: date
  status: str

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
  pH_level: float

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
  method_of_harvest: str

class stock_records(BaseModel):
  pond_name: str
  species: str
  quantity: int
  average_weight: float
  stocking_date: date
  supplier: str
  status: str