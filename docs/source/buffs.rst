genscan.buffs
===========

Buff plugins augment, constrain, or otherwise perturb the interaction
between probes and a generator.  These allow things like mapping
probes into a different language, or expanding prompts to various
paraphrases, and so on.

Buffs must inherit this base class. 
`Buff` serves as a template showing what expectations there are for
implemented buffs.

.. toctree::
   :maxdepth: 2

   genscan.buffs
   genscan.buffs.base
   genscan.buffs.encoding
   genscan.buffs.low_resource_languages
   genscan.buffs.lowercase
   genscan.buffs.paraphrase
