# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest

import genscan._plugins
import genscan.generators.base
import genscan.generators.test

TEST_GENERATORS = [
    a
    for a, b in genscan._plugins.enumerate_plugins("generators")
    if b is True and a.startswith("generators.test")
]


@pytest.mark.parametrize("klassname", TEST_GENERATORS)
def test_test_instantiate(klassname):
    g = genscan._plugins.load_plugin(klassname)
    assert isinstance(g, genscan.generators.base.Generator)


@pytest.mark.parametrize("klassname", TEST_GENERATORS)
def test_test_gen(klassname):
    g = genscan._plugins.load_plugin(klassname)
    for generations in (1, 50):
        out = g.generate("", generations_this_call=generations)
        assert isinstance(out, list), ".generate() must return a list"
        assert (
            len(out) == generations
        ), ".generate() must respect generations_per_call param"
        for s in out:
            assert (
                isinstance(s, str) or s is None
            ), "generate()'s returned list's items must be string or None"
