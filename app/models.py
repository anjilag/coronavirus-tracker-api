"""app.models.py"""
from typing import Dict, List

from pydantic import BaseModel, validator
from abc import ABCMeta, abstractmethod

class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, confirmed, deaths, recovered): pass

class Subject(metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, obs): pass

    @abstractmethod
    def unsubscribe(self, obs): pass

    @abstractmethod
    def notify(self, obs): pass

class Latest(BaseModel, Subject):
    """
    Latest model.
    """

    confirmed: int
    deaths: int
    recovered: int
    subscribers = []
    
    def subscribe(self, obs):
        self.subscribers.append(obs)

    def unsubscribe(self, obs):
        self.subscribers.remove(obs)

    def notify(self):
        for sub in self.subscribers:
            sub.update(self.confirmed, self.deaths, self.recovered)

class LatestResponse(BaseModel, Observer):
    """
    Response for latest.
    """

    confirmed: int
    deaths:int
    recovered:int

    def update(self, confirmed, deaths, recovered):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered


class Timeline(BaseModel):
    """
    Timeline model.
    """

    timeline: Dict[str, int] = {}

    @validator("timeline")
    @classmethod
    def sort_timeline(cls, value):
        """Sort the timeline history before inserting into the model"""
        return dict(sorted(value.items()))

    @property
    def latest(self):
        """Get latest available history value."""
        return list(self.timeline.values())[-1] if self.timeline else 0

    def serialize(self):
        """
        Serialize the model into dict
        TODO: override dict() instead of using serialize
        """
        return {**self.dict(), "latest": self.latest}


class Timelines(BaseModel):
    """
    Timelines model.
    """

    confirmed: Timeline
    deaths: Timeline
    recovered: Timeline


class Location(BaseModel, Observer):
    """
    Location model.
    """

    id: int
    country: str
    country_code: str
    country_population: int = None
    province: str = ""
    county: str = ""
    last_updated: str  # TODO use datetime.datetime type.
    coordinates: Dict
    confirmed: int
    deaths:int
    recovered:int
    timelines: Timelines = {}

    def update(self, confirmed, deaths, recovered):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

class LocationResponse(BaseModel):
    """
    Response for location.
    """

    location: Location


class LocationsResponse(BaseModel):
    """
    Response for locations.
    """

    confirmed:int
    deaths:int
    recovered:int
    locations: List[Location] = []

    def update(self, confirmed, deaths, recovered):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    locations: List[Location] = []
