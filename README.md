# wassupbot
Bot for communicating over whatsapp
This is based on [yowsup echo client](https://github.com/tgalal/yowsup/wiki/Sample-Application). (Please note that this library still needs a lot of work.)
Wit.ai engine is being used as chatbot engine. 




Direct Execution
- Help: run.py -h 
- Bot: run.py -c bot

Dependency: 
- c compiler: gcc or cc
- yowsup package: pip install yowsup2 (a phone number should have been registered. Please check yowsup documentation)
- witai package: pip install wit (The wit.ai app should have been configured and it's api keys added to configuraton.)

Docker Setup & Execution:
This requires docker to setup but will pull out all dependencies.
- Update wassupbot.cfg with all the required information
- run build-image.sh to build the docker image
- run run-image.sh to run the image

