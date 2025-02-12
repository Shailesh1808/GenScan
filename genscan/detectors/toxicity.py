"""
Toxicity detectors
"""

from genscan import _config
from genscan.detectors.base import HFDetector


class ToxicCommentModel(HFDetector):
    """Using backup of martin-ha/toxic-comment-model DistilBERT to detect toxic content"""

    DEFAULT_PARAMS = HFDetector.DEFAULT_PARAMS | {
        "detector_model_path": "genscan-llm/toxic-comment-model",
        "detector_target_class": "toxic",
    }

    bcp47 = "en"
    tags = ["avid-effect:ethics:E0301"]
