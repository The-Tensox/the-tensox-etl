# importing the requests library
import requests
import time
import random
import copy
import cv2
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import matplotlib.pyplot as plt

TEMPLATE_OBJECT = {"id": 1, "position_x": 0, "position_y": 0, "position_z": 0,
                   "rotation_x": 0, "rotation_y": 0, "rotation_z": 0,
                   "scale_x": 0, "scale_y": 0, "scale_z": 0, "mass": 0,
                   "velocity_x": 0, "velocity_y": 0, "velocity_z": 0,
                   "collision_x": 0, "collision_y": 0, "collision_z": 0,
                   "height": 0, "radius": 0, "kind": "random"}

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
    requests.delete(url=URL)


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

    # sending get request and saving the response as response object
    list(map(lambda data: requests.post(url=URL, json=data, headers=headers),
             data_to_send))


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


def heightmap_to_array_mesh(im, position_x=0, position_y=0, position_z=0):
    meshes = []
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            meshes.append({"normals": [0.0, 0.0, 0.0], "uvs": [0.0, 0.0],
                           "vertices": [i * 1.0, im[i, j] * 1.0, j * 1.0]})
    return [{"position_x": position_x,
             "position_y": position_y,
             "position_z": position_z,
             "mesh": {"Array": {"meshes": meshes}}}]


def heightmap_to_cubes(im, position_x, position_y, position_z):
    cubes = []
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            if (i+j)%10!=0:
                continue
            cubes.append({"position_x": position_x + i * 1.0,
                          "position_y": position_y + im[i, j] * 1.0,
                          "position_z": position_z + j * 1.0,
                          "mesh": {"Box": {"x": 1.0, "y": 1.0, "z": 1.0}}})
    return cubes


def image_to_tiles(image_path, nb_tiles, resize=False):
    img = cv2.imread(image_path, 0)
    if resize:
        # img = cv2.resize(img, (img.shape[0] // 8, img.shape[1] // 8))
        img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)
    M = img.shape[0] // nb_tiles
    N = img.shape[1] // nb_tiles
    return [img[x:x+M, y:y+N] for x in range(0, img.shape[0], M) for y in range(0, img.shape[1], N)]


def send_data_to_server(data):
    requests.post(URL, json=data, headers=headers)


def heightmap(mesh=False):
    nb_tiles = 16
    tiles = image_to_tiles("heightmap.png", nb_tiles, True)
    print(tiles[0].shape, len(tiles))
    z = 0
    x = 0
    for i in range(100):
        x = i % nb_tiles # i % new_line * tiles[0].shape[0]
        if i % nb_tiles == 0:
            z += tiles[0].shape[1]
        if mesh:
            data = heightmap_to_array_mesh(tiles[i], x, 0, z)
        else:
            data = heightmap_to_cubes(tiles[i], x, 0, z)
        # [requests.post(url=URL, json=d, headers=headers) for d in data]
        with PoolExecutor(max_workers=200) as executor:
            for _ in executor.map(send_data_to_server, data):
                pass
        print(len(data), "POSTS")


def plot_images():
    images = image_to_tiles("heightmap.png", 8, True)
    fig = plt.figure(figsize=(8, 8))
    columns = 4
    rows = 5
    for i in range(1, columns*rows + 1):
        fig.add_subplot(rows, columns, i)
        plt.imshow(images[i])
    plt.show(block=True)


def main():
    clear_objects()
    # create_grass_and_ground()
    # plot_images()
    heightmap()

    """
    while True:
        create_grass_and_ground()
        time.sleep(5)
        clear_objects()
    """


if __name__ == '__main__':
    main()
