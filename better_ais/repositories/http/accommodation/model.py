from typing import Any
from pydantic import BaseModel

class AccUserResidence(BaseModel):
    dormitory: str
    block: str
    floor: int
    cell: int
    room: int
    cost: float

    def __str__(self):
        return f"{self.dormitory} {self.block} {self.floor}{self.cell}/{self.room} {self.cost}€"


class AccUserPayment(BaseModel):
    iban: str
    swift: str
    variable_symbol: str
    arrears: float
    scan_to_pay_code: str


class AccUser(BaseModel):
    residence: AccUserResidence
    payment: AccUserPayment
    
    @staticmethod
    def from_dataclass(dс: Any):
        return AccUser(
            residence = AccUserResidence(
                **dс.residence.__dict__
            ),
            payment = AccUserPayment(
                **dс.payment.__dict__
            )
        )