# Run the app, mapping your machine’s port 4000 to the container’s EXPOSEd port 80 using -p
# You should see a notice that Python is serving your app at http://0.0.0.0:80. But that message coming from inside the container, 
# which doesn’t know you mapped port 80 of that container to 4000, making the correct URL http://localhost:4000. 
# Go there, and you’ll see the “Hello World” text, the container ID, and the Redis error message.

# This will run interactively. Press CTRL+C to kill
#docker run wassupbot 

# To run in background in detached mode
# to kill, run docker ps and then docker stop containerid
docker run -d wassupbot 
