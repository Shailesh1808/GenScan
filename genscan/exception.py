# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0


class genscanException(Exception):
    """Base class for all  genscan exceptions"""


class APIKeyMissingError(genscanException):
    """Exception to be raised if a required API key is not found"""


class ModelNameMissingError(genscanException):
    """A generator requires model_name to be set, but it wasn't"""


class genscanBackoffTrigger(genscanException):
    """Thrown when backoff should be triggered"""


class PluginConfigurationError(genscanException):
    """Plugin config/description is not usable"""


class BadGeneratorException(PluginConfigurationError):
    """Generator invocation requested is not usable"""


class RateLimitHit(Exception):
    """Raised when a rate limiting response is returned"""


class ConfigFailure(genscanException):
    """Raised when plugin configuration fails"""


class PayloadFailure(genscanException):
    """Problem instantiating/using payloads"""
