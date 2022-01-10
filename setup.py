from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Dataset labelling'
LONG_DESCRIPTION = 'Automated dataset labelling using Detectron2 and Nvidia Deepstream'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="create-dataset", 
        version=VERSION,
        author="Pedro Pablo Correa",
        author_email="<pbcorrea@uc.cl>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "torch==1.10.1",
            "torchvision==0.11.2",
            "detectron2 @ git+https://github.com/facebookresearch/detectron2.git",
            "opencv-python==4.5.5.62",
            "uvicorn==0.16.0",
            "fastapi==0.71.0"
        ], # add any additional packages that 
)