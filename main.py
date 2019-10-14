# importing the requests library 
import requests 
import time
import random

# api-endpoint 
URL = "http://localhost:8001/objects"
  
  


headers = {'Content-type': 'application/json'}

while True:
  # defining a params dict for the parameters to be sent to the API 
  data = {"id":1, "position_x": random.randint(0, 10), "position_y": random.randint(0, 10), "position_z": random.randint(0, 10),
          "rotation_x":0, "rotation_y":0, "rotation_z":0, "scale_x":0, "scale_y":0,
          "scale_z":0, "mass": 0, "velocity_x": 0, "velocity_y": 0, "velocity_z": 0,
          "collision_x": 0, "collision_y": 0, "collision_z": 0, "height": 0, "radius": 0}
  # sending get request and saving the response as response object 
  try:
    r = requests.put(url = URL + '/' + str(data['id']), json = data, headers = headers) 
    # extracting data in json format 
    data = r.json() 
      
    # printing the output 
    print(f"Response {data}") 
  except requests.exceptions.ConnectionError as e:
    print("Url unreachable")
  time.sleep(1)
  
