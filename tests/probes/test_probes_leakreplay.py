# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os

import genscan
import genscan._config
import genscan._plugins
import genscan.attempt
import genscan.cli
import genscan.probes.leakreplay


def test_leakreplay_hitlog():

    args = "-m test.Blank -p leakreplay -d always.Fail".split()
    genscan.cli.main(args)


def test_leakreplay_output_count():
    generations = 1
    genscan._config.load_base_config()
    genscan._config.transient.reportfile = open(os.devnull, "w+")
    genscan._config.plugins.probes["leakreplay"]["generations"] = generations
    a = genscan.attempt.Attempt(prompt="test")
    p = genscan._plugins.load_plugin(
        "probes.leakreplay.LiteratureCloze80", config_root=genscan._config
    )
    g = genscan._plugins.load_plugin("generators.test.Blank", config_root=genscan._config)
    p.generator = g
    results = p._execute_all([a])
    assert len(a.all_outputs) == generations


def test_leakreplay_handle_incomplete_attempt():
    p = genscan.probes.leakreplay.LiteratureCloze80()
    a = genscan.attempt.Attempt(prompt="IS THIS BROKEN")
    a.outputs = ["", None]
    p._postprocess_hook(a)
