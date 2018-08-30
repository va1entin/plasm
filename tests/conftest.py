from nacl import encoding
import pytest
import os

@pytest.fixture
def inputFileHash():
    inputFileHash = '5e7b96b55dcf8ffaf6d3a0f1b862d97a4d507062fa9e5945bd4ef0815cffdc7b'
    return inputFileHash

@pytest.fixture
def inputFileBWHash():
    inputFileBWHash = '7a4a2adc46c2ce33ab8c993f1b2d7928186b5ab53ff2ed439dcc68af649d9af6'
    return inputFileBWHash

@pytest.fixture
def privateKeyName():
    privateKeyName = 'private.key'
    return privateKeyName

@pytest.fixture
def publicKeyName():
    publicKeyName = 'public.key'
    return publicKeyName

@pytest.fixture
def password():
    password = b'test-password123'
    return password

@pytest.fixture
def sampleFile():
    sampleFile = 'img.jpg'
    return sampleFile

@pytest.fixture
def sampleFileBW():
    sampleFileBW = 'img_bw.jpg'
    return sampleFileBW

@pytest.fixture
def sampleDir():
    sampleDir = 'tests/imgs/'
    return sampleDir

@pytest.fixture
def inputFile(sampleDir, sampleFile):
    inputFile = os.path.join(os.getcwd(), sampleDir, sampleFile)
    return inputFile

@pytest.fixture
def inputDir(sampleDir):
    inputDir = os.path.join(os.getcwd(), sampleDir)
    return inputDir

@pytest.fixture
def usedEncoder():
    return encoding.RawEncoder
