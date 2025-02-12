# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os

import genscan._config
import genscan._plugins

import genscan.probes.base
import genscan.probes.fileformats
import genscan.attempt


def test_hf_files_load():
    p = genscan.probes.fileformats.HF_Files()
    assert isinstance(p, genscan.probes.base.Probe)


def test_hf_files_hf_repo():
    p = genscan._plugins.load_plugin("probes.fileformats.HF_Files")
    genscan._config.plugins.generators["huggingface"] = {
        "Model": {"name": "gpt2", "hf_args": {"device": "cpu"}},
    }
    g = genscan._plugins.load_plugin(
        "generators.huggingface.Model", config_root=genscan._config
    )
    r = p.probe(g)
    assert isinstance(r, list), ".probe should return a list"
    assert len(r) == 1, "HF_Files.probe() should return one attempt"
    assert isinstance(
        r[0], genscan.attempt.Attempt
    ), "HF_Files.probe() must return an Attempt"
    assert isinstance(r[0].outputs, list), "File list scan should return a list"
    assert len(r[0].outputs) > 0, "File list scan should return list of filenames"
    for filename in r[0].outputs:
        assert isinstance(
            filename, str
        ), "File list scan should return list of string filenames"
        assert os.path.isfile(filename), "List of HF_Files paths should all be real"
