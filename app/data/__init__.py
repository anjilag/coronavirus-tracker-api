"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from abc import ABCMeta, abstractmethod

# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": JhuLocationService(),
    "csbs": CSBSLocationService(),
    "nyt": NYTLocationService(),
}

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())


class LocationAssembler:
    """The Director"""
    builder = None

    def setBuilder(self,builder):
        self.builder = builder

    def getSource(self):
        product = LocationSource()
        source = self.builder.getDataSource()
        product.setDataSource(source)

class LocationSource:
    """The Product"""
    def __init__(self):
        self.datasource = None

    def setDataSource(self, dataSource):
        self.dataSource = dataSource

class LocationSourceBuilder(metaclass=ABCMeta):
    """The Interface"""
    @abstractmethod
    def getDataSource(self): pass

class JHUBuilder(LocationSourceBuilder):
    """The Concrete Builder"""
    def getDataSource(self):
        return DATA_SOURCES.get("jhu")

class CSBSBuilder(LocationSourceBuilder):
    """The Concrete Builder"""
    def getDataSource(self):
        return DATA_SOURCES.get("csbs")

class NYTBuilder(LocationSourceBuilder):
    """The Concrete Builder"""
    def getDataSource(self):
        return DATA_SOURCES.get("nyt")
