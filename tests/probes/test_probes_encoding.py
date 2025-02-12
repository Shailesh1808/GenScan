# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import genscan.probes.encoding


def test_InjectBase64_len_cap():
    p = genscan.probes.encoding.InjectBase64()
    num_payloads = len(genscan.probes.encoding.payloads)
    num_templates = len(genscan.probes.encoding.TEMPLATES)
    num_encoders = len(p.encoding_funcs)
    assert len(p.prompts) < num_payloads * num_templates * num_encoders


def test_InjectBase64_prompt_trigger_match():
    p = genscan.probes.encoding.InjectBase64()
    num_payloads = len(genscan.probes.encoding.payloads)
    num_templates = len(genscan.probes.encoding.TEMPLATES)
    num_encoders = len(p.encoding_funcs)
    assert len(p.prompts) == len(p.triggers)


def test_InjectBase64_triggers_not_in_prompts():
    p = genscan.probes.encoding.InjectBase64()
    num_payloads = len(genscan.probes.encoding.payloads)
    num_templates = len(genscan.probes.encoding.TEMPLATES)
    num_encoders = len(p.encoding_funcs)
    for i in range(len(p.triggers)):
        assert p.triggers[i] not in p.prompts[i]


def test_encoding_payload_library_size_count():
    genscan.probes.encoding._load_payloads()
    payload_count = len(genscan.probes.encoding.payloads)
    p = genscan.probes.encoding.InjectBase2048()
    assert len(genscan.probes.encoding.payloads) == payload_count
    p = genscan.probes.encoding.InjectZalgo()
    assert len(genscan.probes.encoding.payloads) == payload_count
    p = genscan.probes.encoding.InjectBase64()
    assert len(genscan.probes.encoding.payloads) == payload_count
    genscan.probes.encoding._load_payloads()
    assert len(genscan.probes.encoding.payloads) == payload_count
