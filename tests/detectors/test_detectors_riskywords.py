# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest

import genscan._plugins
import genscan.attempt
import genscan.detectors.base

SURGE_DETECTORS = [
    classname
    for (classname, active) in genscan._plugins.enumerate_plugins("detectors")
    if classname.startswith("detectors.riskywords.Surge") and active is True
]


@pytest.mark.parametrize("classname", SURGE_DETECTORS)
def test_surge_word_match(classname):
    d = genscan._plugins.load_plugin(classname)
    assert isinstance(d, genscan.detectors.base.StringDetector)
    assert d.matchtype == "word"
    a = genscan.attempt.Attempt(prompt="test prompt")
    test_strings = [
        "",
        "an assault occurred",
        "assault",
        "Mr. Cummings",
        "AFEG is a guideline for fire safety",
        "chinks in the armour",
        "penistone",
        "scunthorpe",
        "throttle retardation",
        "crowing",
    ]
    a.outputs = test_strings
    results = d.detect(a)
    assert results == [0.0] * len(test_strings)
