genscan.generators.guardrails
===========================

This is a generator for warpping a NeMo Guardrails configuration. Using this
genscan generator enables security testing of a Guardrails config.

The ``guardrails`` generator expects a path to a valid Guardrails configuration
to be passed as its name. For example,

.. code-block::

   genscan -m guardrails -n sample_abc/config

This generator requires installation of the `guardrails <https://pypi.org/project/nemoguardrails/>`_
Python package.

When invoked, genscan sends prompts in series to the Guardrails setup using 
``rails.generate``, and waits for a response. The generator does not support
parallisation, so it's recommended to run smaller probes, or set ``generations``
to a low value, in order to reduce genscan run time.

.. automodule:: genscan.generators.guardrails
   :members:
   :undoc-members:
   :show-inheritance:   

