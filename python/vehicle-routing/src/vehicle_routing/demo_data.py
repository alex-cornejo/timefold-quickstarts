from typing import Generator
from datetime import date, datetime, time, timedelta
from enum import Enum
from random import Random
from dataclasses import dataclass

from .domain import *


FIRST_NAMES = ("Amy", "Beth", "Chad", "Dan", "Elsa", "Flo", "Gus", "Hugo", "Ivy", "Jay")
LAST_NAMES = ("Cole", "Fox", "Green", "Jones", "King", "Li", "Poe", "Rye", "Smith", "Watt")


@dataclass
class _DemoDataProperties:
    seed: int
    visit_count: int
    vehicle_count: int
    min_demand: int
    max_demand: int
    min_vehicle_capacity: int
    max_vehicle_capacity: int
    south_west_corner: Location
    north_east_corner: Location

    def __post_init__(self):
        if self.min_demand < 1:
            raise ValueError(f"minDemand ({self.min_demand}) must be greater than zero.")
        if self.max_demand < 1:
            raise ValueError(f"maxDemand ({self.max_demand}) must be greater than zero.")
        if self.min_demand >= self.max_demand:
            raise ValueError(f"maxDemand ({self.max_demand}) must be greater than minDemand ({self.min_demand}).")
        if self.min_vehicle_capacity < 1:
            raise ValueError(f"Number of minVehicleCapacity ({self.min_vehicle_capacity}) must be greater than zero.")
        if self.max_vehicle_capacity < 1:
            raise ValueError(f"Number of maxVehicleCapacity ({self.max_vehicle_capacity}) must be greater than zero.")
        if self.min_vehicle_capacity >= self.max_vehicle_capacity:
            raise ValueError(f"maxVehicleCapacity ({self.max_vehicle_capacity}) must be greater than "
                             f"minVehicleCapacity ({self.min_vehicle_capacity}).")
        if self.visit_count < 1:
            raise ValueError(f"Number of visitCount ({self.visit_count}) must be greater than zero.")
        if self.vehicle_count < 1:
            raise ValueError(f"Number of vehicleCount ({self.vehicle_count}) must be greater than zero.")
        if self.north_east_corner.latitude <= self.south_west_corner.latitude:
            raise ValueError(f"northEastCorner.getLatitude ({self.north_east_corner.latitude}) must be greater than "
                             f"southWestCorner.getLatitude({self.south_west_corner.latitude}).")
        if self.north_east_corner.longitude <= self.south_west_corner.longitude:
            raise ValueError(f"northEastCorner.getLongitude ({self.north_east_corner.longitude}) must be greater than "
                             f"southWestCorner.getLongitude({self.south_west_corner.longitude}).")


class DemoData(Enum):
    PHILADELPHIA = _DemoDataProperties(0, 55, 6,
                                       1, 2, 15, 30,
                                       Location(latitude=39.7656099067391,
                                                longitude=-76.83782328143754),
                                       Location(latitude=40.77636644354855,
                                                longitude=-74.9300739430771))

    HARTFORT = _DemoDataProperties(1, 50, 6,
                                   1, 3, 20, 30,
                                   Location(latitude=41.48366520850297,
                                            longitude=-73.15901689943055),
                                   Location(latitude=41.99512052869307,
                                            longitude=-72.25114548877427))

    FIRENZE = _DemoDataProperties(2, 77, 6,
                                  1, 2, 20, 40,
                                  Location(latitude=43.751466,
                                           longitude=11.177210),
                                  Location(latitude=43.809291,
                                           longitude=11.290195))


def doubles(random: Random, start: float, end: float) -> Generator[float, None, None]:
    while True:
        yield random.uniform(start, end)


def ints(random: Random, start: int, end: int) -> Generator[int, None, None]:
    while True:
        yield random.randrange(start, end)


def generate_names(random: Random) -> Generator[str, None, None]:
    while True:
        yield f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}'


def generate_demo_data(demo_data_enum: DemoData) -> VehicleRoutePlan:
    name = "demo"
    demo_data = demo_data_enum.value
    random = Random(demo_data.seed)
    latitudes = doubles(random, demo_data.south_west_corner.latitude, demo_data.north_east_corner.latitude)
    longitudes = doubles(random, demo_data.south_west_corner.longitude, demo_data.north_east_corner.longitude)

    demands = ints(random, demo_data.min_demand, demo_data.max_demand + 1)
    vehicle_capacities = ints(random, demo_data.min_vehicle_capacity,
                              demo_data.max_vehicle_capacity + 1)

    vehicles = [Vehicle(id=str(i),
                        capacity=next(vehicle_capacities),
                        home_location=Location(
                            latitude=next(latitudes),
                            longitude=next(longitudes)))
                for i in range(demo_data.vehicle_count)]

    names = generate_names(random)
    visits = [
        Visit(
             id=str(i),
             name=next(names),
             location=Location(latitude=next(latitudes), longitude=next(longitudes)),
             demand=next(demands)
         ) for i in range(demo_data.visit_count)
    ]

    return VehicleRoutePlan(name=name,
                            south_west_corner=demo_data.south_west_corner,
                            north_east_corner=demo_data.north_east_corner,
                            vehicles=vehicles,
                            visits=visits)


def tomorrow_at(local_time: time) -> datetime:
    return datetime.combine(date.today(), local_time)