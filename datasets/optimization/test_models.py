from __future__ import annotations

from typing import TYPE_CHECKING

from qcportal.datasets.optimization.models import OptimizationDatasetNewEntry
from qcportal.datasets.testing_helpers import (
    run_dataset_model_add_get_entry,
    run_dataset_model_add_entry_duplicate,
    run_dataset_model_delete_entry,
    run_dataset_model_add_get_spec,
    run_dataset_model_add_spec_duplicate,
    run_dataset_model_delete_spec,
    run_dataset_model_remove_record,
    run_dataset_model_submit,
    run_dataset_model_submit_missing,
    run_dataset_model_iterate_updated,
    run_dataset_model_modify_records,
)
from qcportal.molecules import Molecule
from qcportal.records import PriorityEnum
from qcportal.records.optimization.models import OptimizationSpecification, OptimizationProtocols
from qcportal.records.singlepoint.models import QCSpecification

if TYPE_CHECKING:
    from qcportal import PortalClient

test_entries = [
    OptimizationDatasetNewEntry(
        initial_molecule=Molecule(symbols=["h", "h"], geometry=[0, 0, 0, 0, 0, 2]), name="hydrogen_2"
    ),
    OptimizationDatasetNewEntry(
        initial_molecule=Molecule(symbols=["h", "h"], geometry=[0, 0, 0, 0, 0, 4]),
        name="HYDrogen_4",
        comment="a comment",
        attributes={"internal": "h2"},
    ),
    OptimizationDatasetNewEntry(
        initial_molecule=Molecule(symbols=["h", "h"], geometry=[0, 0, 0, 0, 0, 6]),
        name="hydrogen_6",
        additional_keywords={"maxiter": 1234},
    ),
]

test_specs = [
    OptimizationSpecification(
        program="opt_prog_1",
        qc_specification=QCSpecification(
            program="prog1", driver="deferred", method="b3lyp", basis="6-31g*", keywords={"maxiter": 20}
        ),
        keywords={"opt_kw_1": 123, "opt_kw_2": "a string"},
    ),
    OptimizationSpecification(
        program="opt_prog_2",
        qc_specification=QCSpecification(
            program="prog2", driver="deferred", method="hf", basis="sto-3g", keywords={"maxiter": 40}
        ),
        keywords={"opt_kw_1": 456, "opt_kw_2": "another string"},
        protocols=OptimizationProtocols(trajectory="none"),
    ),
    OptimizationSpecification(
        program="opt_prog_3",
        qc_specification=QCSpecification(
            program="prog3", driver="deferred", method="hf", basis="sto-3g", keywords={"maxiter": 40}
        ),
        keywords={"opt_kw_1": 789, "opt_kw_2": "another string 2"},
        protocols=OptimizationProtocols(trajectory="final"),
    ),
]


def entry_extra_compare(ent1, ent2):
    assert ent1.initial_molecule == ent2.initial_molecule


def record_entry_compare(rec, ent):
    assert rec.initial_molecule == ent.initial_molecule


def test_optimization_dataset_model_add_get_entry(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_add_get_entry(snowflake_client, ds, test_entries, entry_extra_compare)


def test_optimization_dataset_model_add_entry_duplicate(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_add_entry_duplicate(snowflake_client, ds, test_entries, entry_extra_compare)


def test_optimization_dataset_model_delete_entry(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_delete_entry(snowflake_client, ds, test_entries, test_specs)


def test_optimization_dataset_model_add_get_spec(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_add_get_spec(snowflake_client, ds, test_specs)


def test_optimization_dataset_model_add_spec_duplicate(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_add_spec_duplicate(snowflake_client, ds, test_specs)


def test_optimization_dataset_model_delete_spec(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_delete_spec(snowflake_client, ds, test_entries, test_specs)


def test_optimization_dataset_model_remove_record(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_remove_record(snowflake_client, ds, test_entries, test_specs)


def test_optimization_dataset_model_submit(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset(
        "optimization", "Test dataset", default_tag="default_tag", default_priority=PriorityEnum.low
    )
    run_dataset_model_submit(ds, test_entries, test_specs[0], record_entry_compare)


def test_optimization_dataset_model_submit_missing(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_submit_missing(ds)


def test_optimization_dataset_model_iterate_updated(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_iterate_updated(ds, test_entries, test_specs[0])


def test_optimization_dataset_model_modify_records(snowflake_client: PortalClient):
    ds = snowflake_client.add_dataset("optimization", "Test dataset")
    run_dataset_model_modify_records(ds, test_entries, test_specs[0])
