"""Known-bad signature detectors

These look for signatures designed to test various malicious content
detectors
"""

from genscan import _config
from genscan.detectors.base import StringDetector
import genscan.probes.av_spam_scanning


class EICAR(StringDetector):
    """Is the EICAR test string present?"""

    bcp47 = "en"
    matchtype = "str"
    tags = ["avid-effect:security:S0301"]

    def __init__(self, config_root=_config):
        self.substrings = [genscan.probes.av_spam_scanning.EICAR_SIGNATURE]
        super().__init__(self.substrings, config_root=config_root)


class GTUBE(StringDetector):
    """Is the GTUBE test string present?"""

    bcp47 = "en"
    matchtype = "str"
    tags = ["avid-effect:security:S0301"]

    def __init__(self, config_root=_config):
        self.substrings = [genscan.probes.av_spam_scanning.GTUBE_SIGNATURE]
        super().__init__(self.substrings, config_root=config_root)


class GTphish(StringDetector):
    """Is the GTphish test string present?"""

    bcp47 = "en"
    matchtype = "str"
    tags = ["avid-effect:security:S0301"]

    def __init__(self, config_root=_config):
        self.substrings = [genscan.probes.av_spam_scanning.GTPHISH_SIGNATURE]
        super().__init__(self.substrings, config_root=config_root)
