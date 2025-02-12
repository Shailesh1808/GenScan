Usage
=====

.. _installation:

Installation
------------

``genscan`` is a command-line tool. It's developed in Linux and OSX.

Friendly install instructions are at `<https://docs.genscan.ai/genscan/llm-scanning-basics/setting-up/installing-genscan>`_ .
The instructions below will work, but you might need to be quite familiar with your OS to use them, because they assume some particular pieces of background knowledge.

Standard quick `pip` install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use genscan, first install it using pip:

.. code-block:: console

   pip install genscan


Install development version with `pip`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The standard pip version of ``genscan`` is updated periodically. To get a fresher version, from GitHub, try:

.. code-block:: console

    python3 -m pip install -U git+https://github.com/NVIDIA/genscan.git@main


For development: clone from `git`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also clone the source and run ``genscan`` directly. This works fine and is recommended for development.

``genscan`` has its own dependencies. You can to install ``genscan`` in its own Conda environment:

.. code-block:: console

    conda create --name genscan "python>=3.10,<=3.12"
    conda activate genscan
    gh repo clone NVIDIA/genscan
    cd genscan
    python3 -m pip install -r requirements.txt

OK, if that went fine, you're probably good to go!


Running genscan
-------------


The general syntax is:

.. code-block:: console

    genscan <options>

``genscan`` needs to know what model to scan, and by default, it'll try all the probes it knows on that model, using the vulnerability detectors recommended by each probe. You can see a list of probes using:

.. code-block:: console

    genscan --list_probes

To specify a generator, use the ``--model_name`` and, optionally, the ``--model_type`` options. 
Model name specifies a model family/interface; model type specifies the exact model to be used. 
The "Intro to generators" section below describes some of the generators supported. 
A straightfoward generator family is Hugging Face models; to load one of these, set ``--model_name`` to ``huggingface`` and ``--model_type`` to the model's name on Hub (e.g. "RWKV/rwkv-4-169m-pile"). 
Some generators might need an API key to be set as an environment variable, and they'll let you know if they need that.

``genscan`` runs all the probes by default, but you can be specific about that too. 
``--probes promptinject`` will use only the `PromptInject <https://github.com/agencyenterprise/promptinject>`_ framework's methods, for example. 
You can also specify one specific plugin instead of a plugin family by adding the plugin name after a ``.``; for example, ``--probes lmrc.SlurUsage`` will use an implementation of checking for models generating slurs based on the `Language Model Risk Cards <https://arxiv.org/abs/2303.18190>`_ framework.


Examples
^^^^^^^^

Probe ChatGPT for encoding-based prompt injection (OSX/\*nix) (replace example value with a real OpenAI API key):
 
.. code-block:: console

    export OPENAI_API_KEY="sk-123XXXXXXXXXXXX"
    genscan --model_type openai --model_name gpt-3.5-turbo --probes encoding


See if the Hugging Face version of GPT2 is vulnerable to DAN 11.0:

.. code-block:: console

    genscan --model_type huggingface --model_name gpt2 --probes dan.Dan_11_0

