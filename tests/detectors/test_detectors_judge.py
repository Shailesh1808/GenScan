# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
import pytest

from genscan.attempt import Attempt
import genscan.detectors.base
import genscan.detectors.judge
from genscan.exception import BadGeneratorException

DETECTOR_CLASSES = [genscan.detectors.judge.ModelAsJudge, genscan.detectors.judge.Refusal]


@pytest.fixture
def judge_config():
    return {
        "detectors": {
            "judge": {
                "detector_model_config": {
                    "api_key": "fake",
                },
            },
        }
    }


@pytest.mark.parametrize("klass", DETECTOR_CLASSES)
def test_class_init(judge_config, klass):
    d = klass(config_root=judge_config)
    assert isinstance(d, genscan.detectors.base.Detector)


@pytest.mark.parametrize("klass", DETECTOR_CLASSES)
def test_model_as_judge_type(klass):
    judge_config = {
        "detectors": {
            "judge": {
                "detector_model_type": "test",
                "detector_model_name": "Test",
            },
        }
    }
    with pytest.raises(BadGeneratorException) as exc_info:
        klass(config_root=judge_config)
    assert "must be compatible with" in str(exc_info.value)


DETECT_TESTS = [
    (genscan.detectors.judge.ModelAsJudge, ["Rating: [[3]]"], 0),
    (genscan.detectors.judge.ModelAsJudge, ["Rating: [[7]]"], 1),
    (genscan.detectors.judge.ModelAsJudge, ["Rating: [[11]]"], 1),
    (genscan.detectors.judge.ModelAsJudge, ["No rating response"], 0),
    (genscan.detectors.judge.Refusal, ["[[NO]]"], 0),
    (genscan.detectors.judge.Refusal, ["[[YES]]"], 1),
    (
        genscan.detectors.judge.Refusal,
        ["Invalid"],
        1,
    ),  # if the judge cannot determine on_topic consider response as refusal
]


@pytest.mark.parametrize("klass, response, res_val", DETECT_TESTS)
def test_klass_detect(judge_config, mocker, klass, response, res_val):
    d = klass(config_root=judge_config)
    mock_generate = mocker.patch.object(
        d.evaluation_generator, "generate", return_value=response
    )
    a = Attempt(probe_classname="test.Test", prompt="test prompt")
    a.outputs = ["fake"]
    res = d.detect(a)
    mock_generate.assert_called_once()
    assert len(a.all_outputs) == len(res)
    assert [res_val * len(a.all_outputs)] == res
