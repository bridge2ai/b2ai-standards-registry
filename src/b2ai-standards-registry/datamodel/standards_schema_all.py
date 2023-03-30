# Auto generated from standards_schema_all.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-03-29T17:14:34
# Schema: standards-schema-all
#
# id: https://w3id.org/bridge2ai/standards-schema-all
# description: High-level classes for Bridge2AI Standards schemas.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
B2AI = CurieNamespace('B2AI', 'https://w3id.org/bridge2ai/standards-schema/')
B2AI_ORG = CurieNamespace('B2AI_ORG', 'https://w3id.org/bridge2ai/standards-organization-schema/')
B2AI_STANDARD = CurieNamespace('B2AI_STANDARD', 'https://w3id.org/bridge2ai/standards-datastandardortool-schema/')
B2AI_SUBSTRATE = CurieNamespace('B2AI_SUBSTRATE', 'https://w3id.org/bridge2ai/standards-datasubstrate-schema/')
B2AI_TOPIC = CurieNamespace('B2AI_TOPIC', 'https://w3id.org/bridge2ai/standards-datatopic-schema/')
B2AI_USECASE = CurieNamespace('B2AI_USECASE', 'https://w3id.org/bridge2ai/standards-usecase-schema/')
MESH = CurieNamespace('MESH', 'http://id.nlm.nih.gov/mesh/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CurieNamespace('', 'https://w3id.org/bridge2ai/standards-schema-all/')


# Types
class CategoryType(Uriorcurie):
    """ A primitive type in which the value denotes a class within the model. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "category_type"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/CategoryType")


class EdamIdentifier(Uriorcurie):
    """ Identifier from EDAM ontology """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "edam_identifier"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/EdamIdentifier")


class MeshIdentifier(Uriorcurie):
    """ Identifier from Medical Subject Headings (MeSH) biomedical vocabulary. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "mesh_identifier"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/MeshIdentifier")


class NcitIdentifier(Uriorcurie):
    """ Identifier from NCIT reference terminology with broad coverage of the cancer domain. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ncit_identifier"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/NcitIdentifier")


class RorIdentifier(Uriorcurie):
    """ Identifier from Research Organization Registry. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ror_identifier"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/RorIdentifier")


class WikidataIdentifier(Uriorcurie):
    """ Identifier from Wikidata open knowledge base. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "wikidata_identifier"
    type_model_uri = URIRef("https://w3id.org/bridge2ai/standards-schema-all/WikidataIdentifier")


# Class references
class NamedThingId(URIorCURIE):
    pass


class DataStandardOrToolId(NamedThingId):
    pass


class DataStandardId(DataStandardOrToolId):
    pass


class BiomedicalStandardId(DataStandardId):
    pass


class RegistryId(DataStandardOrToolId):
    pass


class OntologyOrVocabularyId(DataStandardOrToolId):
    pass


class ModelRepositoryId(DataStandardOrToolId):
    pass


class ReferenceDataOrDatasetId(DataStandardOrToolId):
    pass


class SoftwareOrToolId(DataStandardOrToolId):
    pass


class ReferenceImplementationId(DataStandardOrToolId):
    pass


class TrainingProgramId(DataStandardOrToolId):
    pass


class DataSubstrateId(NamedThingId):
    pass


class DataTopicId(NamedThingId):
    pass


class OrganizationId(NamedThingId):
    pass


class UseCaseId(NamedThingId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to"]

    class_class_uri: ClassVar[URIRef] = SCHEMA.Thing
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/NamedThing")

    id: Union[str, NamedThingId] = None
    category: Optional[Union[str, CategoryType]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    subclass_of: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    related_to: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    contributor_name: Optional[str] = None
    contributor_github_name: Optional[str] = None
    contributor_orcid: Optional[Union[str, URIorCURIE]] = None
    contribution_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.category is not None and not isinstance(self.category, CategoryType):
            self.category = CategoryType(self.category)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.subclass_of, list):
            self.subclass_of = [self.subclass_of] if self.subclass_of is not None else []
        self.subclass_of = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.subclass_of]

        if not isinstance(self.related_to, list):
            self.related_to = [self.related_to] if self.related_to is not None else []
        self.related_to = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.related_to]

        if self.contributor_name is not None and not isinstance(self.contributor_name, str):
            self.contributor_name = str(self.contributor_name)

        if self.contributor_github_name is not None and not isinstance(self.contributor_github_name, str):
            self.contributor_github_name = str(self.contributor_github_name)

        if self.contributor_orcid is not None and not isinstance(self.contributor_orcid, URIorCURIE):
            self.contributor_orcid = URIorCURIE(self.contributor_orcid)

        if self.contribution_date is not None and not isinstance(self.contribution_date, XSDDate):
            self.contribution_date = XSDDate(self.contribution_date)

        super().__post_init__(**kwargs)


@dataclass
class DataStandardOrTool(NamedThing):
    """
    Represents a standard or tool in the Bridge2AI Standards Registry.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.DataStandardOrTool
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:DataStandardOrTool"
    class_name: ClassVar[str] = "DataStandardOrTool"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataStandardOrTool")

    id: Union[str, DataStandardOrToolId] = None
    collection: Optional[Union[Union[str, "StandardsCollectionTag"], List[Union[str, "StandardsCollectionTag"]]]] = empty_list()
    concerns_data_topic: Optional[Union[Union[str, DataTopicId], List[Union[str, DataTopicId]]]] = empty_list()
    has_relevant_organization: Optional[Union[Union[str, OrganizationId], List[Union[str, OrganizationId]]]] = empty_list()
    purpose_detail: Optional[str] = None
    is_open: Optional[Union[bool, Bool]] = None
    requires_registration: Optional[Union[bool, Bool]] = None
    url: Optional[Union[str, URIorCURIE]] = None
    publication: Optional[Union[str, URIorCURIE]] = None
    formal_specification: Optional[Union[str, URIorCURIE]] = None
    not_relevant_to_dgps: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataStandardOrToolId):
            self.id = DataStandardOrToolId(self.id)

        if not isinstance(self.collection, list):
            self.collection = [self.collection] if self.collection is not None else []
        self.collection = [v if isinstance(v, StandardsCollectionTag) else StandardsCollectionTag(v) for v in self.collection]

        if not isinstance(self.concerns_data_topic, list):
            self.concerns_data_topic = [self.concerns_data_topic] if self.concerns_data_topic is not None else []
        self.concerns_data_topic = [v if isinstance(v, DataTopicId) else DataTopicId(v) for v in self.concerns_data_topic]

        if not isinstance(self.has_relevant_organization, list):
            self.has_relevant_organization = [self.has_relevant_organization] if self.has_relevant_organization is not None else []
        self.has_relevant_organization = [v if isinstance(v, OrganizationId) else OrganizationId(v) for v in self.has_relevant_organization]

        if self.purpose_detail is not None and not isinstance(self.purpose_detail, str):
            self.purpose_detail = str(self.purpose_detail)

        if self.is_open is not None and not isinstance(self.is_open, Bool):
            self.is_open = Bool(self.is_open)

        if self.requires_registration is not None and not isinstance(self.requires_registration, Bool):
            self.requires_registration = Bool(self.requires_registration)

        if self.url is not None and not isinstance(self.url, URIorCURIE):
            self.url = URIorCURIE(self.url)

        if self.publication is not None and not isinstance(self.publication, URIorCURIE):
            self.publication = URIorCURIE(self.publication)

        if self.formal_specification is not None and not isinstance(self.formal_specification, URIorCURIE):
            self.formal_specification = URIorCURIE(self.formal_specification)

        if self.not_relevant_to_dgps is not None and not isinstance(self.not_relevant_to_dgps, Bool):
            self.not_relevant_to_dgps = Bool(self.not_relevant_to_dgps)

        super().__post_init__(**kwargs)


@dataclass
class DataStandard(DataStandardOrTool):
    """
    Represents a general purpose standard in the Bridge2AI Standards Registry.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.DataStandard
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:DataStandard"
    class_name: ClassVar[str] = "DataStandard"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataStandard")

    id: Union[str, DataStandardId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataStandardId):
            self.id = DataStandardId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class BiomedicalStandard(DataStandard):
    """
    Represents a standard in the Bridge2AI Standards Registry with particular applications or relevance to clinical or
    biomedical research purposes.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.BiomedicalStandard
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:BiomedicalStandard"
    class_name: ClassVar[str] = "BiomedicalStandard"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/BiomedicalStandard")

    id: Union[str, BiomedicalStandardId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiomedicalStandardId):
            self.id = BiomedicalStandardId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Registry(DataStandardOrTool):
    """
    Represents a resource in the Bridge2AI Standards Registry serving to curate and/or index other resources.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.Registry
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:Registry"
    class_name: ClassVar[str] = "Registry"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/Registry")

    id: Union[str, RegistryId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RegistryId):
            self.id = RegistryId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class OntologyOrVocabulary(DataStandardOrTool):
    """
    A set of concepts and categories, potentially defined or accompanied by their hierarchical relationships.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.OntologyOrVocabulary
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:OntologyOrVocabulary"
    class_name: ClassVar[str] = "OntologyOrVocabulary"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/OntologyOrVocabulary")

    id: Union[str, OntologyOrVocabularyId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyOrVocabularyId):
            self.id = OntologyOrVocabularyId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ModelRepository(DataStandardOrTool):
    """
    Represents a resource in the Bridge2AI Standards Registry serving to curate and store computational models. To be
    a respository, the resource must not index models alone.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.ModelRepository
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:ModelRepository"
    class_name: ClassVar[str] = "ModelRepository"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/ModelRepository")

    id: Union[str, ModelRepositoryId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModelRepositoryId):
            self.id = ModelRepositoryId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ReferenceDataOrDataset(DataStandardOrTool):
    """
    Represents a resource in the Bridge2AI Standards Registry serving as a standardized, reusable data source.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.ReferenceDataOrDataset
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:ReferenceDataOrDataset"
    class_name: ClassVar[str] = "ReferenceDataOrDataset"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/ReferenceDataOrDataset")

    id: Union[str, ReferenceDataOrDatasetId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceDataOrDatasetId):
            self.id = ReferenceDataOrDatasetId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SoftwareOrTool(DataStandardOrTool):
    """
    Represents a piece of software or computational tool in the Bridge2AI Standards Registry.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.SoftwareOrTool
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:SoftwareOrTool"
    class_name: ClassVar[str] = "SoftwareOrTool"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/SoftwareOrTool")

    id: Union[str, SoftwareOrToolId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SoftwareOrToolId):
            self.id = SoftwareOrToolId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ReferenceImplementation(DataStandardOrTool):
    """
    Represents an implementation of one or more standards or tools in the Bridge2AI Standards Registry, whether as a
    full specification in a particular language or as an application to a specific use case.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.ReferenceImplementation
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:ReferenceImplementation"
    class_name: ClassVar[str] = "ReferenceImplementation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/ReferenceImplementation")

    id: Union[str, ReferenceImplementationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceImplementationId):
            self.id = ReferenceImplementationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class TrainingProgram(DataStandardOrTool):
    """
    Represents a training program for skills and experience related to standards or tools in the Bridge2AI Standards
    Registry.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to", "concerns_data_topic", "has_relevant_organization"]

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.TrainingProgram
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:TrainingProgram"
    class_name: ClassVar[str] = "TrainingProgram"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/TrainingProgram")

    id: Union[str, TrainingProgramId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TrainingProgramId):
            self.id = TrainingProgramId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DataStandardOrToolContainer(YAMLRoot):
    """
    A container for DataStandardOrTool(s).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = B2AI_STANDARD.DataStandardOrToolContainer
    class_class_curie: ClassVar[str] = "B2AI_STANDARD:DataStandardOrToolContainer"
    class_name: ClassVar[str] = "DataStandardOrToolContainer"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataStandardOrToolContainer")

    data_standardortools_collection: Optional[Union[Dict[Union[str, DataStandardOrToolId], Union[dict, DataStandardOrTool]], List[Union[dict, DataStandardOrTool]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="data_standardortools_collection", slot_type=DataStandardOrTool, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class DataSubstrate(NamedThing):
    """
    Represents a data substrate for Bridge2AI data. This may be a high-level data structure or a specific
    implementation of that structure. Interpret as "data, in this form or format", as compared to DataStandard, which
    refers to the set of rules defining a standard. For example, data in TSV format is represented as a DataSubstrate
    but the concept of TSV format is a DataStandard.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to"]

    class_class_uri: ClassVar[URIRef] = B2AI_SUBSTRATE.DataSubstrate
    class_class_curie: ClassVar[str] = "B2AI_SUBSTRATE:DataSubstrate"
    class_name: ClassVar[str] = "DataSubstrate"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataSubstrate")

    id: Union[str, DataSubstrateId] = None
    edam_id: Optional[Union[str, EdamIdentifier]] = None
    mesh_id: Optional[Union[str, MeshIdentifier]] = None
    ncit_id: Optional[Union[str, NcitIdentifier]] = None
    metadata_storage: Optional[Union[str, List[str]]] = empty_list()
    file_extensions: Optional[Union[str, List[str]]] = empty_list()
    limitations: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataSubstrateId):
            self.id = DataSubstrateId(self.id)

        if self.edam_id is not None and not isinstance(self.edam_id, EdamIdentifier):
            self.edam_id = EdamIdentifier(self.edam_id)

        if self.mesh_id is not None and not isinstance(self.mesh_id, MeshIdentifier):
            self.mesh_id = MeshIdentifier(self.mesh_id)

        if self.ncit_id is not None and not isinstance(self.ncit_id, NcitIdentifier):
            self.ncit_id = NcitIdentifier(self.ncit_id)

        if not isinstance(self.metadata_storage, list):
            self.metadata_storage = [self.metadata_storage] if self.metadata_storage is not None else []
        self.metadata_storage = [v if isinstance(v, str) else str(v) for v in self.metadata_storage]

        if not isinstance(self.file_extensions, list):
            self.file_extensions = [self.file_extensions] if self.file_extensions is not None else []
        self.file_extensions = [v if isinstance(v, str) else str(v) for v in self.file_extensions]

        if not isinstance(self.limitations, list):
            self.limitations = [self.limitations] if self.limitations is not None else []
        self.limitations = [v if isinstance(v, str) else str(v) for v in self.limitations]

        super().__post_init__(**kwargs)


@dataclass
class DataSubstrateContainer(YAMLRoot):
    """
    A container for DataSubstrates.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = B2AI_SUBSTRATE.DataSubstrateContainer
    class_class_curie: ClassVar[str] = "B2AI_SUBSTRATE:DataSubstrateContainer"
    class_name: ClassVar[str] = "DataSubstrateContainer"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataSubstrateContainer")

    data_substrates_collection: Optional[Union[Dict[Union[str, DataSubstrateId], Union[dict, DataSubstrate]], List[Union[dict, DataSubstrate]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="data_substrates_collection", slot_type=DataSubstrate, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class DataTopic(NamedThing):
    """
    Represents a general data topic for Bridge2AI data or the tools/standards applied to the data.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to"]

    class_class_uri: ClassVar[URIRef] = B2AI_TOPIC.DataTopic
    class_class_curie: ClassVar[str] = "B2AI_TOPIC:DataTopic"
    class_name: ClassVar[str] = "DataTopic"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataTopic")

    id: Union[str, DataTopicId] = None
    edam_id: Optional[Union[str, EdamIdentifier]] = None
    mesh_id: Optional[Union[str, MeshIdentifier]] = None
    ncit_id: Optional[Union[str, NcitIdentifier]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataTopicId):
            self.id = DataTopicId(self.id)

        if self.edam_id is not None and not isinstance(self.edam_id, EdamIdentifier):
            self.edam_id = EdamIdentifier(self.edam_id)

        if self.mesh_id is not None and not isinstance(self.mesh_id, MeshIdentifier):
            self.mesh_id = MeshIdentifier(self.mesh_id)

        if self.ncit_id is not None and not isinstance(self.ncit_id, NcitIdentifier):
            self.ncit_id = NcitIdentifier(self.ncit_id)

        super().__post_init__(**kwargs)


@dataclass
class DataTopicContainer(YAMLRoot):
    """
    A container for DataTopics.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = B2AI_TOPIC.DataTopicContainer
    class_class_curie: ClassVar[str] = "B2AI_TOPIC:DataTopicContainer"
    class_name: ClassVar[str] = "DataTopicContainer"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/DataTopicContainer")

    data_topics_collection: Optional[Union[Dict[Union[str, DataTopicId], Union[dict, DataTopic]], List[Union[dict, DataTopic]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="data_topics_collection", slot_type=DataTopic, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Organization(NamedThing):
    """
    Represents a group or organization related to or responsible for one or more Bridge2AI standards.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to"]

    class_class_uri: ClassVar[URIRef] = B2AI_ORG.Organization
    class_class_curie: ClassVar[str] = "B2AI_ORG:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/Organization")

    id: Union[str, OrganizationId] = None
    ror_id: Optional[Union[str, RorIdentifier]] = None
    wikidata_id: Optional[Union[str, WikidataIdentifier]] = None
    url: Optional[Union[str, URIorCURIE]] = None
    related_to: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)

        if self.ror_id is not None and not isinstance(self.ror_id, RorIdentifier):
            self.ror_id = RorIdentifier(self.ror_id)

        if self.wikidata_id is not None and not isinstance(self.wikidata_id, WikidataIdentifier):
            self.wikidata_id = WikidataIdentifier(self.wikidata_id)

        if self.url is not None and not isinstance(self.url, URIorCURIE):
            self.url = URIorCURIE(self.url)

        if not isinstance(self.related_to, list):
            self.related_to = [self.related_to] if self.related_to is not None else []
        self.related_to = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.related_to]

        super().__post_init__(**kwargs)


@dataclass
class OrganizationContainer(YAMLRoot):
    """
    A container for Organizations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = B2AI_ORG.OrganizationContainer
    class_class_curie: ClassVar[str] = "B2AI_ORG:OrganizationContainer"
    class_name: ClassVar[str] = "OrganizationContainer"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/OrganizationContainer")

    organizations: Optional[Union[Dict[Union[str, OrganizationId], Union[dict, Organization]], List[Union[dict, Organization]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="organizations", slot_type=Organization, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class UseCase(NamedThing):
    """
    Represents a use case for Bridge2AI standards.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of", "related_to"]

    class_class_uri: ClassVar[URIRef] = B2AI_USECASE.UseCase
    class_class_curie: ClassVar[str] = "B2AI_USECASE:UseCase"
    class_name: ClassVar[str] = "UseCase"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/UseCase")

    id: Union[str, UseCaseId] = None
    use_case_category: Union[str, "UseCaseCategory"] = None
    known_limitations: Optional[str] = None
    relevance_to_dgps: Optional[Union[Union[str, "DataGeneratingProject"], List[Union[str, "DataGeneratingProject"]]]] = empty_list()
    data_topics: Optional[Union[Union[str, DataTopicId], List[Union[str, DataTopicId]]]] = empty_list()
    data_substrates: Optional[Union[Union[str, DataSubstrateId], List[Union[str, DataSubstrateId]]]] = empty_list()
    standards_and_tools_for_dgp_use: Optional[Union[Union[str, DataStandardOrToolId], List[Union[str, DataStandardOrToolId]]]] = empty_list()
    alternative_standards_and_tools: Optional[Union[Union[str, DataStandardOrToolId], List[Union[str, DataStandardOrToolId]]]] = empty_list()
    enables: Optional[Union[Union[str, UseCaseId], List[Union[str, UseCaseId]]]] = empty_list()
    involved_in_experimental_design: Optional[Union[bool, Bool]] = None
    involved_in_metadata_management: Optional[Union[bool, Bool]] = None
    involved_in_quality_control: Optional[Union[bool, Bool]] = None
    xref: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UseCaseId):
            self.id = UseCaseId(self.id)

        if self._is_empty(self.use_case_category):
            self.MissingRequiredField("use_case_category")
        if not isinstance(self.use_case_category, UseCaseCategory):
            self.use_case_category = UseCaseCategory(self.use_case_category)

        if self.known_limitations is not None and not isinstance(self.known_limitations, str):
            self.known_limitations = str(self.known_limitations)

        if not isinstance(self.relevance_to_dgps, list):
            self.relevance_to_dgps = [self.relevance_to_dgps] if self.relevance_to_dgps is not None else []
        self.relevance_to_dgps = [v if isinstance(v, DataGeneratingProject) else DataGeneratingProject(v) for v in self.relevance_to_dgps]

        if not isinstance(self.data_topics, list):
            self.data_topics = [self.data_topics] if self.data_topics is not None else []
        self.data_topics = [v if isinstance(v, DataTopicId) else DataTopicId(v) for v in self.data_topics]

        if not isinstance(self.data_substrates, list):
            self.data_substrates = [self.data_substrates] if self.data_substrates is not None else []
        self.data_substrates = [v if isinstance(v, DataSubstrateId) else DataSubstrateId(v) for v in self.data_substrates]

        if not isinstance(self.standards_and_tools_for_dgp_use, list):
            self.standards_and_tools_for_dgp_use = [self.standards_and_tools_for_dgp_use] if self.standards_and_tools_for_dgp_use is not None else []
        self.standards_and_tools_for_dgp_use = [v if isinstance(v, DataStandardOrToolId) else DataStandardOrToolId(v) for v in self.standards_and_tools_for_dgp_use]

        if not isinstance(self.alternative_standards_and_tools, list):
            self.alternative_standards_and_tools = [self.alternative_standards_and_tools] if self.alternative_standards_and_tools is not None else []
        self.alternative_standards_and_tools = [v if isinstance(v, DataStandardOrToolId) else DataStandardOrToolId(v) for v in self.alternative_standards_and_tools]

        if not isinstance(self.enables, list):
            self.enables = [self.enables] if self.enables is not None else []
        self.enables = [v if isinstance(v, UseCaseId) else UseCaseId(v) for v in self.enables]

        if self.involved_in_experimental_design is not None and not isinstance(self.involved_in_experimental_design, Bool):
            self.involved_in_experimental_design = Bool(self.involved_in_experimental_design)

        if self.involved_in_metadata_management is not None and not isinstance(self.involved_in_metadata_management, Bool):
            self.involved_in_metadata_management = Bool(self.involved_in_metadata_management)

        if self.involved_in_quality_control is not None and not isinstance(self.involved_in_quality_control, Bool):
            self.involved_in_quality_control = Bool(self.involved_in_quality_control)

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.xref]

        super().__post_init__(**kwargs)


@dataclass
class UseCaseContainer(YAMLRoot):
    """
    A container for UseCase.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = B2AI_USECASE.UseCaseContainer
    class_class_curie: ClassVar[str] = "B2AI_USECASE:UseCaseContainer"
    class_name: ClassVar[str] = "UseCaseContainer"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/bridge2ai/standards-schema-all/UseCaseContainer")

    use_cases: Optional[Union[Dict[Union[str, UseCaseId], Union[dict, UseCase]], List[Union[dict, UseCase]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="use_cases", slot_type=UseCase, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations
class DataGeneratingProject(EnumDefinitionImpl):
    """
    One of the Bridge2AI Data Generating Projects.
    """
    aireadi = PermissibleValue(text="aireadi",
                                     description="AI-READI: Uncovering the details of how human health is restored after disease, using type 2 diabetes as a model.",
                                     meaning=None)
    chorus = PermissibleValue(text="chorus",
                                   description="CHoRUS: Collaborative Hospital Repository Uniting Standards. Using imaging, clinical, and other data collected in an ICU setting for diagnosis and risk prediction.",
                                   meaning=None)
    cm4ai = PermissibleValue(text="cm4ai",
                                 description="CM4AI: Cell Maps for AI. Mapping spatiotemporal architecture of human cells to interpret cell structure/function in health and disease.",
                                 meaning=None)
    voice = PermissibleValue(text="voice",
                                 description="Voice as a Biomarker of Health: Building an ethically sourced, bioaccoustic database to understand disease like never before.",
                                 meaning=None)

    _defn = EnumDefinition(
        name="DataGeneratingProject",
        description="One of the Bridge2AI Data Generating Projects.",
    )

class StandardsCollectionTag(EnumDefinitionImpl):
    """
    Tags for specific sets of standards.
    """
    audiovisual = PermissibleValue(text="audiovisual",
                                             description="Audiovisual Standard")
    deprecated = PermissibleValue(text="deprecated",
                                           description="Deprecated")
    fileformat = PermissibleValue(text="fileformat",
                                           description="File Format")
    toolkit = PermissibleValue(text="toolkit",
                                     description="Bioinformatics Toolkit")
    clinicaldata = PermissibleValue(text="clinicaldata",
                                               description="Clinical Data")
    multimodal = PermissibleValue(text="multimodal",
                                           description="Multimodal Data Integration")
    text = PermissibleValue(text="text",
                               description="Text Data")
    cloudplatform = PermissibleValue(text="cloudplatform",
                                                 description="Cloud Research Platform")
    cloudservice = PermissibleValue(text="cloudservice",
                                               description="Cloud Service")
    codesystem = PermissibleValue(text="codesystem",
                                           description="Code System")
    datamodel = PermissibleValue(text="datamodel",
                                         description="Data Model")
    dataregistry = PermissibleValue(text="dataregistry",
                                               description="Data Registry")
    softwareregistry = PermissibleValue(text="softwareregistry",
                                                       description="Software Registry")
    datavisualization = PermissibleValue(text="datavisualization",
                                                         description="Data Visualization")
    notebookplatform = PermissibleValue(text="notebookplatform",
                                                       description="Notebook Platform")
    datasheets = PermissibleValue(text="datasheets",
                                           description="Datasheets")
    machinelearningframework = PermissibleValue(text="machinelearningframework",
                                                                       description="Machine Learning Framework")
    workflowlanguage = PermissibleValue(text="workflowlanguage",
                                                       description="Workflow Language")
    diagnosticinstrument = PermissibleValue(text="diagnosticinstrument",
                                                               description="Diagnostic Instrument")
    drugdata = PermissibleValue(text="drugdata",
                                       description="Drug Data")
    eyedata = PermissibleValue(text="eyedata",
                                     description="Eye Data")
    markuplanguage = PermissibleValue(text="markuplanguage",
                                                   description="Markup Language")
    graphdataplatform = PermissibleValue(text="graphdataplatform",
                                                         description="Graph Data Platform")
    guidelines = PermissibleValue(text="guidelines",
                                           description="Guidelines")
    minimuminformationschema = PermissibleValue(text="minimuminformationschema",
                                                                       description="Minimum Information Schema")
    modelcards = PermissibleValue(text="modelcards",
                                           description="Model Cards")
    obofoundry = PermissibleValue(text="obofoundry",
                                           description="OBO Foundry")
    ontologyregistry = PermissibleValue(text="ontologyregistry",
                                                       description="Ontology Registry")
    policy = PermissibleValue(text="policy",
                                   description="Policy")
    proteindata = PermissibleValue(text="proteindata",
                                             description="Protein Data")
    referencegenome = PermissibleValue(text="referencegenome",
                                                     description="Reference Genome")
    scrnaseqanalysis = PermissibleValue(text="scrnaseqanalysis",
                                                       description="scRNA-seq Analysis")
    speechdata = PermissibleValue(text="speechdata",
                                           description="Speech Data")
    standardsregistry = PermissibleValue(text="standardsregistry",
                                                         description="Standards Registry")

    _defn = EnumDefinition(
        name="StandardsCollectionTag",
        description="Tags for specific sets of standards.",
    )

class UseCaseCategory(EnumDefinitionImpl):
    """
    Category of use case.
    """
    acquisition = PermissibleValue(text="acquisition",
                                             description="Acquisition")
    integration = PermissibleValue(text="integration",
                                             description="Integration")
    standardization = PermissibleValue(text="standardization",
                                                     description="Standardization")
    modeling = PermissibleValue(text="modeling",
                                       description="Modeling")
    application = PermissibleValue(text="application",
                                             description="Application")
    assessment = PermissibleValue(text="assessment",
                                           description="Assessment")

    _defn = EnumDefinition(
        name="UseCaseCategory",
        description="Category of use case.",
    )

# Slots
class slots:
    pass

slots.node_property = Slot(uri=B2AI.node_property, name="node_property", curie=B2AI.curie('node_property'),
                   model_uri=DEFAULT_.node_property, domain=NamedThing, range=Optional[str])

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.type = Slot(uri=B2AI.type, name="type", curie=B2AI.curie('type'),
                   model_uri=DEFAULT_.type, domain=NamedThing, range=Optional[str])

slots.category = Slot(uri=B2AI.category, name="category", curie=B2AI.curie('category'),
                   model_uri=DEFAULT_.category, domain=NamedThing, range=Optional[Union[str, CategoryType]])

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=DEFAULT_.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=Optional[str])

slots.edam_id = Slot(uri=B2AI.edam_id, name="edam_id", curie=B2AI.curie('edam_id'),
                   model_uri=DEFAULT_.edam_id, domain=None, range=Optional[Union[str, EdamIdentifier]])

slots.mesh_id = Slot(uri=B2AI.mesh_id, name="mesh_id", curie=B2AI.curie('mesh_id'),
                   model_uri=DEFAULT_.mesh_id, domain=None, range=Optional[Union[str, MeshIdentifier]])

slots.ncit_id = Slot(uri=B2AI.ncit_id, name="ncit_id", curie=B2AI.curie('ncit_id'),
                   model_uri=DEFAULT_.ncit_id, domain=None, range=Optional[Union[str, NcitIdentifier]])

slots.url = Slot(uri=B2AI.url, name="url", curie=B2AI.curie('url'),
                   model_uri=DEFAULT_.url, domain=NamedThing, range=Optional[Union[str, URIorCURIE]])

slots.xref = Slot(uri=B2AI.xref, name="xref", curie=B2AI.curie('xref'),
                   model_uri=DEFAULT_.xref, domain=NamedThing, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.contributor_name = Slot(uri=B2AI.contributor_name, name="contributor_name", curie=B2AI.curie('contributor_name'),
                   model_uri=DEFAULT_.contributor_name, domain=NamedThing, range=Optional[str])

slots.contributor_github_name = Slot(uri=B2AI.contributor_github_name, name="contributor_github_name", curie=B2AI.curie('contributor_github_name'),
                   model_uri=DEFAULT_.contributor_github_name, domain=NamedThing, range=Optional[str])

slots.contributor_orcid = Slot(uri=B2AI.contributor_orcid, name="contributor_orcid", curie=B2AI.curie('contributor_orcid'),
                   model_uri=DEFAULT_.contributor_orcid, domain=NamedThing, range=Optional[Union[str, URIorCURIE]])

slots.contribution_date = Slot(uri=B2AI.contribution_date, name="contribution_date", curie=B2AI.curie('contribution_date'),
                   model_uri=DEFAULT_.contribution_date, domain=NamedThing, range=Optional[Union[str, XSDDate]])

slots.related_to = Slot(uri=B2AI.related_to, name="related_to", curie=B2AI.curie('related_to'),
                   model_uri=DEFAULT_.related_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.subclass_of = Slot(uri=B2AI.subclass_of, name="subclass_of", curie=B2AI.curie('subclass_of'),
                   model_uri=DEFAULT_.subclass_of, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.collection = Slot(uri=B2AI_STANDARD.collection, name="collection", curie=B2AI_STANDARD.curie('collection'),
                   model_uri=DEFAULT_.collection, domain=NamedThing, range=Optional[Union[Union[str, "StandardsCollectionTag"], List[Union[str, "StandardsCollectionTag"]]]])

slots.purpose_detail = Slot(uri=B2AI_STANDARD.purpose_detail, name="purpose_detail", curie=B2AI_STANDARD.curie('purpose_detail'),
                   model_uri=DEFAULT_.purpose_detail, domain=NamedThing, range=Optional[str])

slots.is_open = Slot(uri=B2AI_STANDARD.is_open, name="is_open", curie=B2AI_STANDARD.curie('is_open'),
                   model_uri=DEFAULT_.is_open, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.requires_registration = Slot(uri=B2AI_STANDARD.requires_registration, name="requires_registration", curie=B2AI_STANDARD.curie('requires_registration'),
                   model_uri=DEFAULT_.requires_registration, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.concerns_data_topic = Slot(uri=B2AI_STANDARD.concerns_data_topic, name="concerns_data_topic", curie=B2AI_STANDARD.curie('concerns_data_topic'),
                   model_uri=DEFAULT_.concerns_data_topic, domain=DataStandardOrTool, range=Optional[Union[Union[str, DataTopicId], List[Union[str, DataTopicId]]]])

slots.publication = Slot(uri=B2AI_STANDARD.publication, name="publication", curie=B2AI_STANDARD.curie('publication'),
                   model_uri=DEFAULT_.publication, domain=NamedThing, range=Optional[Union[str, URIorCURIE]])

slots.formal_specification = Slot(uri=B2AI_STANDARD.formal_specification, name="formal_specification", curie=B2AI_STANDARD.curie('formal_specification'),
                   model_uri=DEFAULT_.formal_specification, domain=NamedThing, range=Optional[Union[str, URIorCURIE]])

slots.has_relevant_organization = Slot(uri=B2AI_STANDARD.has_relevant_organization, name="has_relevant_organization", curie=B2AI_STANDARD.curie('has_relevant_organization'),
                   model_uri=DEFAULT_.has_relevant_organization, domain=DataStandardOrTool, range=Optional[Union[Union[str, OrganizationId], List[Union[str, OrganizationId]]]])

slots.data_standardortools_collection = Slot(uri=B2AI_STANDARD.data_standardortools_collection, name="data_standardortools_collection", curie=B2AI_STANDARD.curie('data_standardortools_collection'),
                   model_uri=DEFAULT_.data_standardortools_collection, domain=None, range=Optional[Union[Dict[Union[str, DataStandardOrToolId], Union[dict, DataStandardOrTool]], List[Union[dict, DataStandardOrTool]]]])

slots.not_relevant_to_dgps = Slot(uri=B2AI_STANDARD.not_relevant_to_dgps, name="not_relevant_to_dgps", curie=B2AI_STANDARD.curie('not_relevant_to_dgps'),
                   model_uri=DEFAULT_.not_relevant_to_dgps, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.metadata_storage = Slot(uri=B2AI_SUBSTRATE.metadata_storage, name="metadata_storage", curie=B2AI_SUBSTRATE.curie('metadata_storage'),
                   model_uri=DEFAULT_.metadata_storage, domain=NamedThing, range=Optional[Union[str, List[str]]])

slots.file_extensions = Slot(uri=B2AI_SUBSTRATE.file_extensions, name="file_extensions", curie=B2AI_SUBSTRATE.curie('file_extensions'),
                   model_uri=DEFAULT_.file_extensions, domain=NamedThing, range=Optional[Union[str, List[str]]])

slots.limitations = Slot(uri=B2AI_SUBSTRATE.limitations, name="limitations", curie=B2AI_SUBSTRATE.curie('limitations'),
                   model_uri=DEFAULT_.limitations, domain=NamedThing, range=Optional[Union[str, List[str]]])

slots.data_substrates_collection = Slot(uri=B2AI_SUBSTRATE.data_substrates_collection, name="data_substrates_collection", curie=B2AI_SUBSTRATE.curie('data_substrates_collection'),
                   model_uri=DEFAULT_.data_substrates_collection, domain=None, range=Optional[Union[Dict[Union[str, DataSubstrateId], Union[dict, DataSubstrate]], List[Union[dict, DataSubstrate]]]])

slots.data_topics_collection = Slot(uri=B2AI_TOPIC.data_topics_collection, name="data_topics_collection", curie=B2AI_TOPIC.curie('data_topics_collection'),
                   model_uri=DEFAULT_.data_topics_collection, domain=None, range=Optional[Union[Dict[Union[str, DataTopicId], Union[dict, DataTopic]], List[Union[dict, DataTopic]]]])

slots.ror_id = Slot(uri=B2AI_ORG.ror_id, name="ror_id", curie=B2AI_ORG.curie('ror_id'),
                   model_uri=DEFAULT_.ror_id, domain=None, range=Optional[Union[str, RorIdentifier]])

slots.wikidata_id = Slot(uri=B2AI_ORG.wikidata_id, name="wikidata_id", curie=B2AI_ORG.curie('wikidata_id'),
                   model_uri=DEFAULT_.wikidata_id, domain=None, range=Optional[Union[str, WikidataIdentifier]])

slots.organizations = Slot(uri=B2AI_ORG.organizations, name="organizations", curie=B2AI_ORG.curie('organizations'),
                   model_uri=DEFAULT_.organizations, domain=None, range=Optional[Union[Dict[Union[str, OrganizationId], Union[dict, Organization]], List[Union[dict, Organization]]]])

slots.use_case_category = Slot(uri=B2AI_USECASE.use_case_category, name="use_case_category", curie=B2AI_USECASE.curie('use_case_category'),
                   model_uri=DEFAULT_.use_case_category, domain=NamedThing, range=Optional[Union[str, "UseCaseCategory"]])

slots.known_limitations = Slot(uri=B2AI_USECASE.known_limitations, name="known_limitations", curie=B2AI_USECASE.curie('known_limitations'),
                   model_uri=DEFAULT_.known_limitations, domain=NamedThing, range=Optional[str])

slots.relevance_to_dgps = Slot(uri=B2AI_USECASE.relevance_to_dgps, name="relevance_to_dgps", curie=B2AI_USECASE.curie('relevance_to_dgps'),
                   model_uri=DEFAULT_.relevance_to_dgps, domain=None, range=Optional[Union[Union[str, "DataGeneratingProject"], List[Union[str, "DataGeneratingProject"]]]])

slots.data_topics = Slot(uri=B2AI_USECASE.data_topics, name="data_topics", curie=B2AI_USECASE.curie('data_topics'),
                   model_uri=DEFAULT_.data_topics, domain=NamedThing, range=Optional[Union[Union[str, DataTopicId], List[Union[str, DataTopicId]]]])

slots.data_substrates = Slot(uri=B2AI_USECASE.data_substrates, name="data_substrates", curie=B2AI_USECASE.curie('data_substrates'),
                   model_uri=DEFAULT_.data_substrates, domain=NamedThing, range=Optional[Union[Union[str, DataSubstrateId], List[Union[str, DataSubstrateId]]]])

slots.standards_and_tools_for_dgp_use = Slot(uri=B2AI_USECASE.standards_and_tools_for_dgp_use, name="standards_and_tools_for_dgp_use", curie=B2AI_USECASE.curie('standards_and_tools_for_dgp_use'),
                   model_uri=DEFAULT_.standards_and_tools_for_dgp_use, domain=NamedThing, range=Optional[Union[Union[str, DataStandardOrToolId], List[Union[str, DataStandardOrToolId]]]])

slots.alternative_standards_and_tools = Slot(uri=B2AI_USECASE.alternative_standards_and_tools, name="alternative_standards_and_tools", curie=B2AI_USECASE.curie('alternative_standards_and_tools'),
                   model_uri=DEFAULT_.alternative_standards_and_tools, domain=NamedThing, range=Optional[Union[Union[str, DataStandardOrToolId], List[Union[str, DataStandardOrToolId]]]])

slots.enables = Slot(uri=B2AI_USECASE.enables, name="enables", curie=B2AI_USECASE.curie('enables'),
                   model_uri=DEFAULT_.enables, domain=NamedThing, range=Optional[Union[Union[str, UseCaseId], List[Union[str, UseCaseId]]]])

slots.involved_in_experimental_design = Slot(uri=B2AI_USECASE.involved_in_experimental_design, name="involved_in_experimental_design", curie=B2AI_USECASE.curie('involved_in_experimental_design'),
                   model_uri=DEFAULT_.involved_in_experimental_design, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.involved_in_metadata_management = Slot(uri=B2AI_USECASE.involved_in_metadata_management, name="involved_in_metadata_management", curie=B2AI_USECASE.curie('involved_in_metadata_management'),
                   model_uri=DEFAULT_.involved_in_metadata_management, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.involved_in_quality_control = Slot(uri=B2AI_USECASE.involved_in_quality_control, name="involved_in_quality_control", curie=B2AI_USECASE.curie('involved_in_quality_control'),
                   model_uri=DEFAULT_.involved_in_quality_control, domain=NamedThing, range=Optional[Union[bool, Bool]])

slots.use_cases = Slot(uri=B2AI_USECASE.use_cases, name="use_cases", curie=B2AI_USECASE.curie('use_cases'),
                   model_uri=DEFAULT_.use_cases, domain=None, range=Optional[Union[Dict[Union[str, UseCaseId], Union[dict, UseCase]], List[Union[dict, UseCase]]]])

slots.UseCase_use_case_category = Slot(uri=B2AI_USECASE.use_case_category, name="UseCase_use_case_category", curie=B2AI_USECASE.curie('use_case_category'),
                   model_uri=DEFAULT_.UseCase_use_case_category, domain=UseCase, range=Union[str, "UseCaseCategory"])