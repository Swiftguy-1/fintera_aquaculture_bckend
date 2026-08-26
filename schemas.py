from pydantic import BaseModel
from datetime import date as date_type, time as time_type
from typing import Optional


class Feed_inventory(BaseModel):
    feed_name: str | None = None
    feed_type: str | None = None
    quantity: int | None = None
    av_weight_per_bag: float | None = None
    feed_cost_per_bag: float | None = None
    feed_total_cost: float | None = None
    supplier: str | None = None
    expiry_date: date_type | None = None
    purchase_date: date_type | None = None
    status: str | None = None


class ponds(BaseModel):
    pond_name: str|None = None
    pond_stock_quantity: float|None = None
    species_in_pond: str|None = None
    last_harvest_date: date_type|None = None
    pond_type: str|None = None
    pond_location: str|None = None
    pond_status: str|None = None
    water_temp: str|None = None
    pond_capacity: float|None = None
    pH_level: float|None = None


class Expenses(BaseModel):
    date: date_type | None = None
    category: str | None = None
    description: str | None = None
    amount: float | None = None
    status: str | None = None


class Sales(BaseModel):
    date: date_type
    customer: str|None = None
    species: str|None = None
    cost: float|None = None
    quantity: int|None = None
    total_weight: float|None = None
    profit: float|None = None
    status: str|None = None


class mortality(BaseModel):
    Mortality_count: int| None = None
    pond_name: str|None = None
    suspected_cause: str|None = None
    species: str|None = None


class harvest(BaseModel):
    pond_name: str |None = None
    species: str|None = None
    harvest_quantity: int|None = None
    total_weight: float|None = None
    harvest_date: date_type|None = None
    method_of_harvest: str|None = None


class stock_records(BaseModel):
    pond_name: str |None = None
    species: str |None = None
    quantity: int|None = None
    average_weight: float|None = None
    stocking_date: date_type|None = None
    supplier: str|None = None
    status: str|None = None


class feeding_logs(BaseModel):
    pond_name: str | None = None
    species: str | None = None
    feed_type: str | None = None
    feed_quantity: int | None = None
    feeding_date: date_type | None = None
    feed_cost: float | None = None


class invoices(BaseModel):
    customer: str |None = None
    date: date_type|None = None
    due_date: date_type|None = None
    amount: int|None = None
    status: str|None = None


class feeding_schedule(BaseModel):
    pond_name: str | None = None
    species: str | None = None
    feed_type: str | None = None
    target_amount: int | None = None
    feeding_time: time_type | None = None
    frequency: str | None = None
    is_active: bool | None = None
    note: Optional[str] = None


class growth_rate(BaseModel):
    pond_name: str | None = None
    species: str | None = None
    sample_date: date_type | None = None
    sample_count: int | None = None
    avg_weight: float | None = None
    total_feed_used: int | None = None
    feed_conversion_rate: float | None = None
    specific_growth_rate: float | None = None
