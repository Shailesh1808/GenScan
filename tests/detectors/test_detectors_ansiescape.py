# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import genscan.attempt
import genscan.detectors.base
import genscan.probes.ansiescape
from genscan import _plugins


def test_ansiescape_raw_load():
    d = _plugins.load_plugin("detectors.ansiescape.Raw")
    assert isinstance(d, genscan.detectors.base.Detector)


def test_ansiescape_raw_strings():
    d = _plugins.load_plugin("detectors.ansiescape.Raw")
    for payload in genscan.probes.ansiescape.LIVE_PAYLOADS:
        a = genscan.attempt.Attempt()
        a.prompt = "test prompt"
        a.outputs = [payload]
        assert d.detect(a) == [1.0], f"{payload} contains a raw control string"
    for payload in genscan.probes.ansiescape.ESCAPED_PAYLOADS:
        a = genscan.attempt.Attempt()
        a.prompt = "test prompt"
        a.outputs = [payload]
        assert d.detect(a) == [0.0], f"{payload} only contains escaped control string"


def test_ansiescape_escaped_load():
    d = _plugins.load_plugin("detectors.ansiescape.Escaped")
    assert isinstance(d, genscan.detectors.base.Detector)


def test_ansiescape_escaped_strings():
    d = _plugins.load_plugin("detectors.ansiescape.Escaped")
    for payload in genscan.probes.ansiescape.ESCAPED_PAYLOADS:
        a = genscan.attempt.Attempt()
        a.prompt = "test prompt"
        a.outputs = [payload]
        assert d.detect(a) == [1.0], f"{payload} contains escaped control string"
    for payload in genscan.probes.ansiescape.LIVE_PAYLOADS:
        a = genscan.attempt.Attempt()
        a.prompt = "test prompt"
        a.outputs = [payload]
        assert d.detect(a) == [0.0], f"{payload} only contains raw control string"
