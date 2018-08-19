import pytest
import os

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
    password = 'test-password123'
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
