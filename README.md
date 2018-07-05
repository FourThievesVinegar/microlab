# FTVC Microlab

![Four Thieves Vinegar Micro Lab](https://github.com/FourThievesVinegar/microlab/blob/master/images/4tvc.jpg)


This is the software component for controlling and monitoring the Four Thieves Vinegar Collective's Apothecary Microlab hardware. It's built for Raspberry Pi using Python 3.6 for the API and controller service layer and JavaScript for the UI.

This is beta software and is under active development.

For more information about the project, visit our website: https://fourthievesvinegar.org/

## Running the Software

It is advised you're using a virtualenv. Then install all the deps in `requirements.txt`:

    pip install -r requirements.txt

From the microlab root directory, just run the following command to run the Flask microservice layer.

    FLASK_DEBUG=true ./run.py

The API will be running at `localhost:5000`.

## Software Architecture

![Micro Lab Software Architecture](https://github.com/FourThievesVinegar/microlab/blob/master/images/SWArch.png)

## Hardware

STL files for building the 3D-printed microlab equipment can be found here https://github.com/FourThievesVinegar/Parts

