from pyoos.utils.etree import etree
from owslib.namespaces import Namespaces
from owslib.util import testXMLValue
from owslib.util import nspath as nsp
from owslib.util import nspath_eval as nspv
from owslib.crs import Crs
from shapely.geometry import box

ns = Namespaces()

class IoosGetObservation(object):
    def __new__(cls, element):
        if isinstance(element, str):
            self._root = etree.fromstring(element)
        else:
            self._root = element

        if hasattr(self._root, 'getroot'):
            self._root = self._root.getroot()

        XLINK_NS = ns.get_namespace("xlink")
        GML_NS = [ns.get_versioned_namespace('gml','3.1.1')]
        version = None
        for g in GML_NS:
            try:
                version = testXMLValue(self._root.find(nsp("{%s}metaDataProperty[{%s}title]/{%s}version" % (GML_NS, XLINK_NS, GML_NS))))
                break
            except:
                continue

        if version == "1.0":
            from pyoos.parsers.ioos.one.get_observation import IoosGetObservation_1_0
            return super(IoosGetObservation, cls).__new__(IoosGetObservation_1_0, element=self._root)
        else:
            raise ValueError("Unsupported IOOS version.  Supported: [1.0]")

    def __init__(self, element):
        # Get individual om:Observations has a hash or name:ob
        self.observations = []
