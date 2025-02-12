import os
import pytest
import tempfile
import genscan.generators.ggml

STORED_ENV = os.getenv(genscan.generators.ggml.ENV_VAR)
MODEL_NAME = None


@pytest.fixture(autouse=True)
def set_fake_env() -> None:
    os.environ[genscan.generators.ggml.ENV_VAR] = os.path.abspath(__file__)


def test_init_bad_app():
    with pytest.raises(RuntimeError) as exc_info:
        del os.environ[genscan.generators.ggml.ENV_VAR]
        genscan.generators.ggml.GgmlGenerator(MODEL_NAME)
    assert "not provided by environment" in str(exc_info.value)


def test_init_missing_model():
    model_name = tempfile.TemporaryFile().name
    with pytest.raises(FileNotFoundError) as exc_info:
        genscan.generators.ggml.GgmlGenerator(model_name)
    assert "File not found" in str(exc_info.value)


def test_init_bad_model():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix="_test_model.gguf", encoding="utf-8", delete=False
    ) as file:
        file.write(file.name)
        file.close()
        with pytest.raises(RuntimeError) as exc_info:
            genscan.generators.ggml.GgmlGenerator(file.name)
        os.remove(file.name)
        assert "not in GGUF" in str(exc_info.value)


def test_init_good_model():
    with tempfile.NamedTemporaryFile(suffix="_test_model.gguf", delete=False) as file:
        file.write(genscan.generators.ggml.GGUF_MAGIC)
        file.close()
        g = genscan.generators.ggml.GgmlGenerator(file.name)
        os.remove(file.name)
        assert type(g) is genscan.generators.ggml.GgmlGenerator
