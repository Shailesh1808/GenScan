# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import genscan.probes.packagehallucination


def test_promptcount():
    languages = {
        "Python": genscan.probes.packagehallucination.Python(),
        "Ruby": genscan.probes.packagehallucination.Ruby(),
        "JavaScript": genscan.probes.packagehallucination.JavaScript(),
        "Rust": genscan.probes.packagehallucination.Rust()
    }

    expected_count = len(genscan.probes.packagehallucination.stub_prompts) * len(
        genscan.probes.packagehallucination.code_tasks
    )

    for language in languages:
        language_probe = languages[language]
        assert (
            len(language_probe.prompts) == expected_count
        ), f"{language} prompt count mismatch. Expected {expected_count}, got {len(language_probe.prompts)}"
