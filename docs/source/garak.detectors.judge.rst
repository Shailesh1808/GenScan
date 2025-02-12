genscan.detectors.judge
==================================

Implements LLM as a Judge.

This works by instantiating an LLM via the generator interface, which will act as the judge.
Judge LLMs need to support the OpenAI API within genscan, i.e. they should inherit OpenAICompatible.
This includes OpenAI, NIM, Azure and Groq generators.


.. automodule:: genscan.detectors.judge
   :members:
   :undoc-members:
   :show-inheritance:   

