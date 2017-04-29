# This will run interactively. Press CTRL+C to kill
# the configuration file should contain all relevant information
# docker run wassupbot 

# To run in background / detached mode (-d)
# to kill, run docker ps and then docker stop containerid
export WA_PASSWORD='YOUR PASSWORD'
export CHAT_ENGINE_KEY='YOUR KEY'
docker run -d -e WA_PHONE='YOUR NUMBER' -e WA_PASSWORD -e CHAT_ENGINE_KEY wassupbot 
