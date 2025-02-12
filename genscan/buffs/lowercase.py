# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

""" Buff that converts prompts to lower case. """

from collections.abc import Iterable

import genscan.attempt
from genscan.buffs.base import Buff


class Lowercase(Buff):
    """Lowercasing buff"""

    def transform(
        self, attempt: genscan.attempt.Attempt
    ) -> Iterable[genscan.attempt.Attempt]:
        attempt.prompt = attempt.prompt.lower()
        yield attempt
