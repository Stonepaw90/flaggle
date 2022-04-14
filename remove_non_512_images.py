#Make a copy of all
#call it "all-512"
#remove "States of the united states" and "index.html"
#Then run this file

import os
print(os.listdir("all-512"))

for country in os.listdir("all-512"):
    for image in os.listdir(f"all-512\\{country}"):
        if image != "512.png":
            os.remove(f"all-512\\{country}\\{image}")