# importing the requests library 
import requests 
import time
import random
import copy

TEMPLATE_OBJECT = {"id": 1, "position_x": 0, "position_y": 0, "position_z": 0,
                   "rotation_x":0, "rotation_y":0, "rotation_z":0, "scale_x": 0, "scale_y": 0,
                   "scale_z": 0, "mass": 0, "velocity_x": 0, "velocity_y": 0, "velocity_z": 0,
                   "collision_x": 0, "collision_y": 0, "collision_z": 0, "height": 0, "radius": 0, "kind": ""}

# api-endpoint 
URL = "http://localhost:8001/objects"
headers = {'Content-type': 'application/json'}

def get_random_position(obj, min, max):
  """
  Takes an object, randomize its position and return it
  """
  obj["position_x"] = random.randint(min, max)
  obj["position_y"] = random.randint(min, max)
  obj["position_z"] = random.randint(min, max)
  return obj

def clear_objects():
  """
  DELETE all objects in the database
  """
  r = requests.get(url = URL, headers = headers) 
  for o in r.json():
    requests.delete(url = URL + '/' + str(o["id"]))

def create_grass_and_ground(dispersal=10):
  """
  Spawn some random stuff
  """
  # defining a params dict for the parameters to be sent to the API 
  # We need to do a deep copy otherwise all object will have the same value
  ground = copy.deepcopy(TEMPLATE_OBJECT)
  ground["kind"] = "ground"
  ground["scale_x"] = 10
  ground["scale_z"] = 10

  grass = copy.deepcopy(TEMPLATE_OBJECT)
  grass["kind"] = "grass"
  grass["scale_x"] = 1
  grass["scale_z"] = 1
  grass["scale_y"] = 1

  data_to_send = [ground] + list(map(lambda _: get_random_position(copy.deepcopy(grass), -dispersal, dispersal), range(10)))
  #print(data_to_send)
  # sending get request and saving the response as response object 
  list(map(lambda data: requests.post(url = URL, json = data, headers = headers), data_to_send))

def create_cube_and_move_random():
  while True:
    # defining a params dict for the parameters to be sent to the API 
    data = copy.deepcopy(TEMPLATE_OBJECT)
    data = get_random_position(data, -10, 10)
    data["kind"] = "ground"
    data["scale_x"] = 1
    data["scale_z"] = 1
    data["scale_y"] = 1
    # sending get request and saving the response as response object 
    try:
      r = requests.put(url = URL + '/' + str(data['id']), json = data, headers = headers) 
      # extracting data in json format 
      if r.status_code == 200:
        data = r.json() 
        
        # printing the output 
        print(f"Response {data}") 
      else:
        print("Unknown object, creating it")
        r = requests.post(url = URL, json = data, headers = headers) 
        # extracting data in json format 
        if r.status_code == 200:
          data = r.json() 
          
          # printing the output 
          print(f"Response {data}") 
    except:
      print("Url unreachable")
    time.sleep(1)





def main():
  clear_objects()
  create_grass_and_ground()
  """
  while True:
    create_grass_and_ground()
    time.sleep(5)
    clear_objects()
  """


if __name__ == '__main__':
  main()