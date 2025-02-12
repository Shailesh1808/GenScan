# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import csv
import tempfile
import types

import pytest

import genscan._config
import genscan.exception
import genscan.payloads


PAYLOAD_NAMES = list(
    genscan.payloads.Director().search()
)  # default includes local custom payloads to help test them


@pytest.mark.parametrize("payload_name", PAYLOAD_NAMES)
def test_core_payloads(payload_name):
    l = genscan.payloads.Director()
    p = l.load(payload_name)
    assert isinstance(
        p, genscan.payloads.PayloadGroup
    ), f"Not a valid payload: {payload_name}"


@pytest.fixture(scope="module")
def payload_typology():
    types = []
    with open(
        genscan.payloads.PAYLOAD_DIR / ".." / "typology_payloads.tsv",
        "r",
        encoding="utf-8",
    ) as typology_file:
        r = csv.reader(typology_file, delimiter="\t")
        for row in r:
            types.append(row[0])
    return types


def test_payload_Director():
    l = genscan.payloads.Director()
    assert isinstance(l, genscan.payloads.Director)


def test_payload_list():
    l = genscan.payloads.Director()
    for payload_name in l.search():
        assert isinstance(
            payload_name, str
        ), "Payload names from Director().search() must be strings"


@pytest.mark.parametrize("payload_name", PAYLOAD_NAMES)
def test_payloads_have_valid_tags(payload_name, payload_typology):
    l = genscan.payloads.Director()
    p = l.load(payload_name)
    for typee in p.types:
        assert (
            typee in payload_typology
        ), f"Payload {payload_name} type {typee} not found in payload typology"


def test_nonexistent_payload_direct_load():
    with pytest.raises(genscan.exception.genscanException):
        genscan.payloads.Director._load_payload("jkasfohgi")


def test_nonexistent_payload_manager_load():
    l = genscan.payloads.Director()
    with pytest.raises(genscan.exception.PayloadFailure):
        p = l.load("mydeardoctor")


def test_non_json_direct_load():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as t:
        with pytest.raises(
            genscan.exception.PayloadFailure
        ):  # blank file aint valid json
            genscan.payloads.Director._load_payload("jkasfohgi", t.name)


OK_PAYLOADS = [
    {"genscan_payload_name": "test", "payloads": ["pay", "load"], "payload_types": []},
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "payload_types": [],
        "bcp47": "en",
    },
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "payload_types": [],
        "detector_name": "detector",
    },
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "payload_types": [],
        "detector_name": "",
    },
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "payload_types": [],
        "detector_name": "llmaaj",
        "detector_config": {"model": "x"},
    },
]

BAD_PAYLOADS = [
    {"genscan_payload_name": "test"},
    {"payloads": ["pay", "load"]},
    {"payload_strings": ["pay", "load"]},
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "payload_types": "Security circumvention instructions",
    },
    {"genscan_payload_name": "test", "payloads": ["pay", "load"], "lang": "en"},
    {"genscan_payload_name": "test", "payloads": ["pay", "load"], "detector_params": {}},
    {"genscan_payload_name": "test", "payloads": ["pay", "load"], "detector_config": {}},
    {
        "genscan_payload_name": "test",
        "payloads": ["pay", "load"],
        "detector_name": "",
        "detector_config": {"model": "x"},
    },
]


@pytest.mark.parametrize("payload", OK_PAYLOADS)
def test_payload_schema_validation_ok(payload):
    assert genscan.payloads._validate_payload(payload) is True


@pytest.mark.parametrize("payload", BAD_PAYLOADS)
def test_payload_schema_validation_bad(payload):
    assert genscan.payloads._validate_payload(payload) != True


def test_filtering():
    l = genscan.payloads.Director()
    assert (
        len(list(l.search(types=["Security"]))) > 0
    ), "There's at least one payload with a type starting 'Security'"
    assert (
        len(
            list(
                l.search(
                    types=[
                        "Security circumvention instructions/Product activation codes"
                    ],
                    include_children=False,
                )
            )
        )
        > 0
    ), "There's at least one payload with this type"
    assert (
        len(list(l.search(types=["Security"], include_children=False))) == 0
    ), "Security isn't a top-level type"
    assert (
        len(list(l.search(types=["Security"], include_children=True))) > 0
    ), "There's at least one payload with a type starting 'Security'"


def test_module_load():
    assert isinstance(genscan.payloads.load("slur_terms_en"), genscan.payloads.PayloadGroup)


def test_module_search():
    assert isinstance(genscan.payloads.search(""), types.GeneratorType)
