Changed frontend folder structure so that all app related code sits under an src folder, this includes the code for the pages (which sits under app as before), and code for styles. I also moved the components folder into the app, prefixed with a _ to signify that it is not a route. This is common convention that I use in my Next.js apps.

Changed backend folder structure so that the app folder contains a "routes" folder, where each route will now be described by a folder, each with the files within named by convention as to what they do. This is to move the file structure more to how I structure my Next.js apps, with each web endpoint being described by a folder.

removed the hello router so as to keep all files in the repo on target

added the icon field to the Source model as optional, so that the code may add the icon later without the serialization to json not being validated correctly

ive made the icon finding functionality and optimized it a little bit, but ideally it would update the json with the icon so that it doesnt need to go and find it every time. I may come back to it later if I have the time

while not strictly necessary, I put the backend link in the env file to follow good frontend developer practice.
you may recreate it by having an env file with the line NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 

Spent less time on the frontend than I wanted due to time constraints, but im pretty happy with how it looks. Used Sass as I do in my normal web app making, with the style folder structure laid out like I normally would in a more fleshed out app. 

Added types reflecting the types in the backend to keep some kind of contract when fetching data. Ideally the schema would be hosted somewhere else for the frontend and backend to read from, so we wouldnt have to update in multiple places, but we dont need to do that for an exercise like this.

Spent a good chunk of time having to go recompile the frontend, as the make function would hot reload the backend, but knock over the frontend. 