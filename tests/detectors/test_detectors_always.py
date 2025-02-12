# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest

from genscan.attempt import Attempt
import genscan._plugins
import genscan.detectors.base
import genscan.detectors.always

ALWAYS_DETECTOR_NAMES = [
    classname
    for (classname, active) in genscan._plugins.enumerate_plugins("detectors")
    if ".always." in classname
]


@pytest.mark.parametrize("detectorname", ALWAYS_DETECTOR_NAMES)
def test_load(detectorname):
    d = genscan._plugins.load_plugin(detectorname)
    assert isinstance(d, genscan.detectors.base.Detector)


def test_fail():
    d = genscan._plugins.load_plugin("detectors.always.Fail")
    a = Attempt(prompt="")
    a.outputs = [""]
    d.detect(a)
    assert d.detect(a) == [1.0]


def test_pass():
    d = genscan._plugins.load_plugin("detectors.always.Pass")
    a = Attempt(prompt="")
    a.outputs = [""]
    assert d.detect(a) == [0.0]


def test_passthru():
    d = genscan._plugins.load_plugin("detectors.always.Passthru")
    a = Attempt(prompt="")
    a.outputs = [""]
    a.detector_results = {"always.Fail": [0.5]}
    assert d.detect(a) == [0.5]
