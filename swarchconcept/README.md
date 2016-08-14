1. High Level Overview
2. Microservices
3. Main Service
4. UIs
5. 4TVC file
6. Rough Plan



---------------------------------------



#1. High Level Overview

![alt text](https://raw.githubusercontent.com/TheDukeZip/4tvc/master/images/SWArch.png?token=AC5VT-rhLo5_JwbFw8s9zjrFx_8vZkrHks5XuRdswA%3D%3D "SW Architecture Concept")

Create microservices that each independently control one function of the hardware. Each services exposes a simple API (mostly RPC, in some cases RESTful... JSON or something else simple) to perform operations with the hardware, and in some cases view or edit the configuration for that piece of hardware.

One microservice to access your saved 4TVC files (see below.) We can probably just have a directory on the filesystem to maintain the files, no need to have a database to store them. Provides ability to see what pharmaceutical files you have, import new ones, search the SD card for new files to import.

Why microservices instead of modules or classes within one big piece of software? I'm not necessarily opposed to that methodology either, but imagine the possibility of expanding to controlling multiple networked machines from one UI. We add an authentication (and authorization) mechanism to the services, and now you can network multiple machines, control them from one master controller service (and one UI) and now you can manufacture double quantities, or prepare two solutions simultaneously with two machines, speeding up your manufacturing process. Or have the possibility of adding an additional machine with unique capabilities into the mix at a later date without mucking around with the whole SW arch. We would have to add some UI screens to configure the networked machines, but the base SW arch would already support it.

One master controller service that is responsible for exposing an API to any user interface that shows what pharmaceuticals are available to produce, send instructions to be displayed to the user for the next step, and perform the correct operations with the hardware (by calling the microservices) for each step as the user indicates they are ready to execute. Also exposes an API to directly perform individual operations with the hardware for testing and diagnostic purposes.

A diagnostic UI to individually test each hardware component when you first construct your machine to make sure everything is working right. "Depress Syringe 1", "Retract Syringe 1", "Turn on stirrer", etc. The diagnostic UI also potentially allows the user to tune the settings for the PID controller for the temperature service.

A Web based UI hosted on the Pi with a low footprint (nginx?) that can be used directly on the Pi if you have a monitor and mouse connected, but could also be remotely accessed from a PC if the Pi is networked. Displays to the user what pharmaceuticals are available. After selecting one, it guides the user through the process step by step, and as the user ackowledges readiness, performs the next operation, with a countdown timer until the next step. For each step, potentially shows the user what "should have happened" or a picture of what the result should look like. Can also display instructions for the user to manually perform that cannot be automated, such as spreading the result out and letting it air dry, purification steps... Initially targets desktop sized browser but could easily be modified to support running on a touch screen TFT display for standalone operation on the Pi if performance is good enough.

Potentially a desktop app that performs the same operations over a USB connection to the Pi so you don't have to network it. A service will run on the Pi that translates instructions over the USB port into API calls to the main service and sends back the results over the USB connection.

A standalone UI that could run directly on the Pi if connected to a touch screen TFT display so no computer is needed. Potentially this could just be a browser in 'kiosk mode' running the Web UI and we'd just need to make sure it looks OK at the smaller resolution.

Create a file format (.4tvc? Maybe someone has a more creative file extention idea) that contains all the information needed to produce an individual pharmaceutical. Probably like to keep it open and easy to read such as XML, and encode any necessary binary data in Base64.

From what I've gathered timing doesn't have to be ultra precise, so in most cases we can likely get away with a modern high level language to accelerate development. Python and node.js at a minimum have bindings for the Pi's GPIO... we could even consider C# using mono (Just think about how many people around the world know .NET...) but haven't looked into if mono support the Pi I/O. Brandon also suggested we can always wrap the Pi interfaces if necessary which is a great idea.



#2. Microservices

* Syringes

  * Push a solution into the mason jar, or retract to load a new syringe. Automatically stops the motor upon receiving input from the microswitches that the plunger is fully depressed or retracted.

  * Methods

    * Depress (Parameters: syringe #, speed(if supported by HW))
    * Retract (Parameters: syringe #, speed(if supported by HW))
    * Get current state (Parameter: one or more syringe #s)

  * Hardware Interfaces

    * Forward
    * Reverse
    * Forward stop switch
    * Reverse stop switch 

* Temperature

  * PID controller to maintain a specific temperature in the mason jar. Need to test if the performance of the Pi will perform PID decently on solutions with the specific heat we're dealing with. Looks like some people on the internet have had success with water based stuff but Ugl1tomato raised a good point about the Pi and timing. A little research shows the Pi has difficulty with single digit millisecond timing but I'm thinking we don't need to deal with timing at such a fine resolution. Also maintains a file containing the individual PID settings so they can be tweaked.

  * Methods

    * Heat (Parameter: temperature)
    * Off
    * Get current temperature
    * Set PID settings
    * Get PID settings

  * Hardware Interfaces

    * Heater
    * Thermistor

* Stirrer

  * Controls the stirring tool

  * Methods

    * On (Parameter: speed(if supported by HW or potentially PWM))
    * Off
    * Get current state

* Files

  * RESTful, provides access to your saved 4TVC files, ability to import new ones

  * Methods (do most of these in a RESTful way but listing them as generalizations)

    * List
    * Import (POST)
    * Delete
    * Load (GET)
    * Update
    * Search SD card
    * Import from SD card (Parameter: filename)



#3. Main Service

I feel like this is somewhat explained in the High Level Overview, if I have time I can add verbage to this section later.



#4. UIs

##Diagnostic UI

![alt text](https://raw.githubusercontent.com/TheDukeZip/4tvc/master/images/Diagnostics.png?token=AC5VT1xcVtFHkOJ2CVuZr8dWlEFgHJbNks5XuRetwA%3D%3D "Diagnostic UI Concept")

##Web UI

![alt text](https://raw.githubusercontent.com/TheDukeZip/4tvc/master/images/Main.png?token=AC5VTz85Kiir1O400YGNIBk3nL4NIkE_ks5XuRfZwA%3D%3D "Main Page Concept")

![alt text](https://raw.githubusercontent.com/TheDukeZip/4tvc/master/images/Start.png?token=AC5VT1VShAVrXQxZBvK3R249Oa8CSqSxks5XuRfzwA%3D%3D "Start Process Concept")


#5. 4TVC File (Go ahead and come up with a more creative name)

Contains all the instructions for manufacturing one pharmaceudical. These instructions are both machine instructions, and instructions that should be displayed to the user for each step of the process.

Probably should keep in an open format such as XML, could even be a JSON file.

Metadata (many fields could be optional)

  * Common Name ("Aspirin")
  * Technical Name ("Acetylsalicylic Acid")
  * Abbreviation ("ACA")
  * Version of 4TVC File ("1.0")
  * Date of 4TVC File ("2016-01-01")
  * Photo to be displayed on the UI along with the name (Base64 or Base16 encoded)
  * .mol data so a UI could potentially render the molecule (Maybe just ASCII or Base64 encoded)
  * Description
    * en-US	Description of the pharma, pre-plan and tag all text to be displayed to user with an IETF language code so additional languages can be added to file later
  * Formula - diagram of all the reactions
  * Array of names of chemicals / solvents needed along with amounts
  * Amount of result expected to produce
  * Source / Credit ("Chematica")

Procedure

  * Array of steps - each step may contain 

    * Instructions to be displayed to the user before proceding along with an optional picture (all text tagged with IETF language code)
    * A set of hardware instructions	(Instructions would represent things like "Depress syringe 1", "Set heater to 40 C", "Wait until reaches 40 C for 2 minutes", "Depress syringe 2", "Turn off heater", "Wait until temperature reaches 28C") Need ways to represent "do this THEN do this" vs "do this WHILE doing this." Each instruction could optionally have a little text to tell the user what is happening.
    * Expected length of time to completion so UI can display a countdown timer
    * Instructions to be displayed to the user after the step completes, along with an optional picture (text tagged with IETF language code)



#6. Rough Plan

Create the microservices for each of the hardware components, along with a basic master controller service that exposes the diagnostic APIs. Then create the diagnostic UI where you can manually operate all the hardware operations, giving base proof of concept with the new hardware. This is where we can fine tune individual hardware services, see how the Pi handles operating all this equipment simultaneously. Work all the kinks with the hardware and hardware interfaces out here.

Then dial in the file format along with the API on the master controller service to step through all the operations. Build the Web UI on top of that and you have a full guided method of actually producing something.

At this point you theoretically have a "Beta" release unless we run into serious performance problems on the Pi. We can evaluate where we're at and potentially queue up some of the other UI ideas as needed.

