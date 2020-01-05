from plasm import common
import pytest
import os

@pytest.fixture
def custom_outfile_extension():
    custom_outfile_extension = '.foobar'
    return custom_outfile_extension

@pytest.fixture
def input_file_hash():
    input_file_hash = '5e7b96b55dcf8ffaf6d3a0f1b862d97a4d507062fa9e5945bd4ef0815cffdc7b'
    return input_file_hash

@pytest.fixture
def input_file_bw_hash():
    input_file_bw_hash = '7a4a2adc46c2ce33ab8c993f1b2d7928186b5ab53ff2ed439dcc68af649d9af6'
    return input_file_bw_hash

@pytest.fixture
def private_key_name():
    private_key_name = 'private.key'
    return private_key_name

@pytest.fixture
def public_key_name():
    public_key_name = 'public.key'
    return public_key_name

@pytest.fixture
def password():
    password = 'test-password123'
    return password

@pytest.fixture
def sample_file():
    sample_file = 'img.jpg'
    return sample_file

@pytest.fixture
def sample_file_bw():
    sample_file_bw = 'img_bw.jpg'
    return sample_file_bw

@pytest.fixture
def sample_dir():
    sample_dir = 'tests/imgs/'
    return sample_dir

@pytest.fixture
def input_file(sample_dir, sample_file):
    input_file = os.path.join(os.getcwd(), sample_dir, sample_file)
    return input_file

@pytest.fixture
def input_dir(sample_dir):
    input_dir = os.path.join(os.getcwd(), sample_dir)
    return input_dir

@pytest.fixture
def used_encoder():
    return common.used_encoder
