from typing import Dict, Any, Union, Optional, List, Iterable, Tuple, Set

from pydantic import BaseModel
from typing_extensions import Literal

from qcportal.molecules import Molecule
from qcportal.records.singlepoint import SinglepointRecord, QCSpecification
from qcportal.utils import make_list
from ..models import BaseDataset


class SinglepointDatasetNewEntry(BaseModel):
    name: str
    comment: Optional[str] = None
    molecule: Union[Molecule, int]
    additional_keywords: Dict[str, Any] = {}
    attributes: Dict[str, Any] = {}


class SinglepointDatasetEntry(SinglepointDatasetNewEntry):
    molecule_id: int
    molecule: Optional[Molecule] = None
    local_results: Optional[Dict[str, Any]] = None


class SinglepointDatasetSpecification(BaseModel):
    name: str
    specification: QCSpecification
    description: Optional[str] = None


class SinglepointDatasetRecordItem(BaseModel):
    entry_name: str
    specification_name: str
    record_id: int
    record: Optional[SinglepointRecord._DataModel]


class SinglepointDataset(BaseDataset):
    class _DataModel(BaseDataset._DataModel):
        dataset_type: Literal["singlepoint"] = "singlepoint"

        specifications: Dict[str, SinglepointDatasetSpecification] = {}
        entries: Dict[str, SinglepointDatasetEntry] = {}
        record_map: Dict[Tuple[str, str], SinglepointRecord] = {}

        contributed_values: Any

    # This is needed for disambiguation by pydantic
    dataset_type: Literal["singlepoint"] = "singlepoint"
    raw_data: _DataModel

    # Needed by the base class
    _entry_type = SinglepointDatasetEntry
    _specification_type = SinglepointDatasetSpecification
    _record_item_type = SinglepointDatasetRecordItem
    _record_type = SinglepointRecord

    @staticmethod
    def transform_entry_includes(includes: Optional[Iterable[str]]) -> Optional[Set[str]]:
        """
        Transforms user-friendly includes into includes used by the web API
        """

        if includes is None:
            return None

        ret = BaseDataset.transform_entry_includes(includes)

        if "molecule" in includes:
            ret.add("molecule")

        return ret

    def add_specification(self, name: str, specification: QCSpecification, description: Optional[str] = None):

        payload = SinglepointDatasetSpecification(name=name, specification=specification, description=description)

        self.client._auto_request(
            "post",
            f"v1/datasets/singlepoint/{self.id}/specifications",
            List[SinglepointDatasetSpecification],
            None,
            None,
            [payload],
            None,
        )

        self._post_add_specification(name)

    def add_entries(self, entries: Union[SinglepointDatasetNewEntry, Iterable[SinglepointDatasetNewEntry]]):

        entries = make_list(entries)
        self.client._auto_request(
            "post",
            f"v1/datasets/singlepoint/{self.id}/entries/bulkCreate",
            List[SinglepointDatasetNewEntry],
            None,
            None,
            entries,
            None,
        )

        new_names = [x.name for x in entries]
        self._post_add_entries(new_names)
