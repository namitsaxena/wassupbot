# The image will try to run the bot (will ERROR without proper configuration)

# This will run interactively. Press CTRL+C to kill
# the configuration file should contain all relevant information
#docker run wassupbot 

# To run in background / detached mode add (-d)
# to kill, run docker ps and then docker stop containerid
export WA_PASSWORD='YOUR PASSWORD'
export CHAT_ENGINE_KEY='YOUR KEY'
docker run -e WA_PHONE='000' -e WA_PASSWORD -e CHAT_ENGINE_KEY wassupbot 
