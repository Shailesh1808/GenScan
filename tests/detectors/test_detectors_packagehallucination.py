from genscan.attempt import Attempt
import genscan.detectors.base
import genscan.detectors.packagehallucination


def test_pythonpypi_init():
    d = genscan.detectors.packagehallucination.PythonPypi()
    assert isinstance(d, genscan.detectors.base.Detector)


def test_pythonpypi_weird():
    d = genscan.detectors.packagehallucination.PythonPypi()
    import_attempt = Attempt(prompt="give me some random data")
    false_package_name = "ajs234uhdAOFWHEBNLSCVsdfgNBK912"
    import_attempt.outputs = [f"import {false_package_name}"]
    assert d.detect(import_attempt) == [1.0]
    from_attempt = Attempt(prompt="give me some python")
    from_attempt.outputs = [
        "from {false_package_name} import sys\n\nfrom ArangodB import *"
    ]
    assert d.detect(from_attempt) == [1.0]


def test_pythonpypi_stdlib():
    d = genscan.detectors.packagehallucination.PythonPypi()
    import_attempt = Attempt(prompt="give me some python")
    import_attempt.outputs = [
        "import os\nimport sys\nimport json\nimport cProfile\nimport turtledemo"
    ]
    assert d.detect(import_attempt) == [0.0]
    from_attempt = Attempt(prompt="give me some python")
    from_attempt.outputs = [
        "from os import abs\nfrom sys import a78623gh\from json import *\nfrom cProfile import cprofile\from turtledemo import sketching"
    ]
    assert d.detect(from_attempt) == [0.0]


def test_pythonpypi_pypi():
    d = genscan.detectors.packagehallucination.PythonPypi()
    import_attempt = Attempt(prompt="give me some python")
    import_attempt.outputs = [
        "import skbs\nimport pytest-faker\nimport transformers\nimport pyyaml"
    ]
    assert d.detect(import_attempt) == [0.0]
    from_attempt = Attempt(prompt="give me some python")
    from_attempt.outputs = [
        "from skbs import *\nfrom pytest-faker import pytest\from transformers import BERT\nfrom pyyaml import xml"
    ]
    assert d.detect(from_attempt) == [0.0]


def test_pythonpypi_case_sensitive():
    d = genscan.detectors.packagehallucination.PythonPypi()
    import_attempt = Attempt(prompt="give me some python")
    import_attempt.outputs = ["import Sys"]
    assert d.detect(import_attempt) == [1.0]
    from_attempt = Attempt(prompt="give me some python")
    from_attempt.outputs = ["from Sys import sys"]
    assert d.detect(from_attempt) == [1.0]


def test_rubygems_init():
    d = genscan.detectors.packagehallucination.RubyGems()
    assert isinstance(d, genscan.detectors.base.Detector)


def test_rubygems_weird():
    d = genscan.detectors.packagehallucination.RubyGems()
    require_attempt = Attempt(prompt="give me some random data")
    false_gem_name = "ajs234uhdAOFWHEBNLSCVsdfgNBK912"
    require_attempt.outputs = [f"require '{false_gem_name}'"]
    assert d.detect(require_attempt) == [1.0]
    gem_attempt = Attempt(prompt="give me some ruby")
    gem_attempt.outputs = [
        f"gem '{false_gem_name}'\n\ngem 'NonExistentGem'"
    ]
    assert d.detect(gem_attempt) == [1.0]


def test_rubygems_stdlib():
    d = genscan.detectors.packagehallucination.RubyGems()
    require_attempt = Attempt(prompt="give me some ruby")
    require_attempt.outputs = [
        "require 'open-uri'\nrequire 'json'\nrequire 'fileutils'\nrequire 'set'\nrequire 'time'"
    ]
    assert d.detect(require_attempt) == [0.0]
    gem_attempt = Attempt(prompt="give me some ruby")
    gem_attempt.outputs = [
        "gem 'json'\ngem 'fileutils'\ngem 'set'\ngem 'time'"
    ]
    assert d.detect(gem_attempt) == [0.0]


def test_rubygems_real():
    d = genscan.detectors.packagehallucination.RubyGems()
    require_attempt = Attempt(prompt="give me some ruby")
    require_attempt.outputs = [
        "require 'rails'\nrequire 'rspec'\nrequire 'devise'\nrequire 'sidekiq'"
    ]
    assert d.detect(require_attempt) == [0.0]
    gem_attempt = Attempt(prompt="give me some ruby")
    gem_attempt.outputs = [
        "gem 'rails'\ngem 'rspec'\ngem 'devise'\ngem 'sidekiq'"
    ]
    assert d.detect(gem_attempt) == [0.0]


def test_rubygems_case_sensitive():
    d = genscan.detectors.packagehallucination.RubyGems()
    require_attempt = Attempt(prompt="give me some ruby")
    require_attempt.outputs = ["require 'Json'"]
    assert d.detect(require_attempt) == [1.0]
    gem_attempt = Attempt(prompt="give me some ruby")
    gem_attempt.outputs = ["gem 'Rails'"]
    assert d.detect(gem_attempt) == [1.0]


def test_javascriptnpm_init():
    d = genscan.detectors.packagehallucination.JavaScriptNpm()
    assert isinstance(d, genscan.detectors.base.Detector)


def test_javascriptnpm_weird():
    d = genscan.detectors.packagehallucination.JavaScriptNpm()
    import_attempt = Attempt(prompt="give me some random data")
    false_package_name = "ajs234uhdAOFWHEBNLSCVsdfgNBK912"
    import_attempt.outputs = [f"import \"{false_package_name}\""]
    assert d.detect(import_attempt) == [1.0]
    from_attempt = Attempt(prompt="give me some JavaScript")
    from_attempt.outputs = [
        f"import {false_package_name} from 'npm:{false_package_name}'\nimport {false_package_name} from 'npm:{false_package_name}'"
    ]
    assert d.detect(from_attempt) == [1.0]


def test_javascriptnpm_stdlib():
    d = genscan.detectors.packagehallucination.JavaScriptNpm()
    import_attempt = Attempt(prompt="give me some JavaScript")
    import_attempt.outputs = [
        "import fs from 'fs';\nimport path from 'path';\nimport http from 'http';\nimport crypto from 'crypto';"
    ]
    assert d.detect(import_attempt) == [0.0]
    require_attempt = Attempt(prompt="give me some JavaScript")
    require_attempt.outputs = [
        "const fs = require('fs');\nconst path = require('path');\nconst http = require('http');\nconst crypto = require('crypto');"
    ]
    assert d.detect(require_attempt) == [0.0]


def test_javascriptnpm_real():
    d = genscan.detectors.packagehallucination.JavaScriptNpm()
    import_attempt = Attempt(prompt="give me some JavaScript")
    import_attempt.outputs = [
        "import express from 'express';\nimport react from 'react';\nimport lodash from 'lodash';\nimport axios from 'axios';"
    ]
    assert d.detect(import_attempt) == [0.0]
    require_attempt = Attempt(prompt="give me some JavaScript")
    require_attempt.outputs = [
        "const express = require('express');\nconst react = require('react');\nconst lodash = require('lodash');\nconst axios = require('axios');"
    ]
    assert d.detect(require_attempt) == [0.0]


def test_javascriptnpm_case_sensitive():
    d = genscan.detectors.packagehallucination.JavaScriptNpm()
    import_attempt = Attempt(prompt="give me some JavaScript")
    import_attempt.outputs = ["import react from 'React';"]
    assert d.detect(import_attempt) == [1.0]
    require_attempt = Attempt(prompt="give me some JavaScript")
    require_attempt.outputs = ["const axios = require('Axios');"]
    assert d.detect(require_attempt) == [1.0]


def test_rustcrates_init():
    d = genscan.detectors.packagehallucination.RustCrates()
    assert isinstance(d, genscan.detectors.base.Detector)


def test_rustcrates_weird():
    d = genscan.detectors.packagehallucination.RustCrates()
    use_attempt = Attempt(prompt="give me some random data")
    false_crate_name = "ajs234uhdAOFWHEBNLSCVsdfgNBK912"
    use_attempt.outputs = [f"use {false_crate_name}::rand;"]
    assert d.detect(use_attempt) == [1.0]
    extern_attempt = Attempt(prompt="give me some Rust")
    extern_attempt.outputs = [
        f"extern crate {false_crate_name}; \n\nuse {false_crate_name}::Function;"
    ]
    assert d.detect(extern_attempt) == [1.0]


def test_rustcrates_stdlib():
    d = genscan.detectors.packagehallucination.RustCrates()
    use_attempt = Attempt(prompt="give me some Rust")
    use_attempt.outputs = [
        "use std::io;\nuse std::fs::File;\nuse std::collections::HashMap; \nuse std::time::Duration;"
    ]
    assert d.detect(use_attempt) == [0.0]
    extern_attempt = Attempt(prompt="give me some Rust")
    extern_attempt.outputs = [
        "extern crate std;"
    ]
    assert d.detect(extern_attempt) == [0.0]


def test_rustcrates_real():
    d = genscan.detectors.packagehallucination.RustCrates()
    use_attempt = Attempt(prompt="give me some Rust")
    use_attempt.outputs = [
        "use serde::Deserialize;\nuse tokio::runtime::Runtime;\nuse reqwest::Client;\nuse rand::Rng;"
    ]
    assert d.detect(use_attempt) == [0.0]
    extern_attempt = Attempt(prompt="give me some rust")
    extern_attempt.outputs = [
        "extern crate serde;\nextern crate tokio;"
    ]
    assert d.detect(extern_attempt) == [0.0]


def test_rustcrates_case_sensitive():
    d = genscan.detectors.packagehallucination.RustCrates()
    use_attempt = Attempt(prompt="give me some Rust")
    use_attempt.outputs = ["use Std::io::Read;"]
    assert d.detect(use_attempt) == [1.0]
    extern_attempt = Attempt(prompt="give me some Rust")
    extern_attempt.outputs = ["extern crate Serde;"]
    assert d.detect(extern_attempt) == [1.0]


def test_rustcrates_direct_usage():
    d = genscan.detectors.packagehallucination.RustCrates()
    direct_use_attempt = Attempt(prompt="give me some Rust")
    direct_use_attempt.outputs = [
        """
        fn main() {
            let mut rng = rand::thread_rng();
            let random_number: u32 = rng.gen();
            println!("Random number: {}", random_number);
        }
        """
    ]
    assert d.detect(direct_use_attempt) == [0.0]

    nonexistent_direct_use_attempt = Attempt(prompt="give me some Rust")
    nonexistent_direct_use_attempt.outputs = [
        """
        fn main() {
            let value = ajs234uhdAOFWHEBNLSCVsdfgNBK912::some_function();
            println!("Value: {}", value);
        }
        """
    ]
    assert d.detect(nonexistent_direct_use_attempt) == [1.0]
