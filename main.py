
from random import random
import overlap
import numpy as np
import csv

from sklearn.neighbors import radius_neighbors_graph

np.random.seed(1)
NUMBER_OF_CUBES = 26
NUMBER_OF_SAMPLES = 10000

SPHERE_MAXIMUM_RADIUS = 10
SPHERE_MAXIMUM_CENTER_VALUE = 5


def random_points_generator(number_of_points):
    maximum_coordinate_value = SPHERE_MAXIMUM_CENTER_VALUE

    points = (np.random.rand(number_of_points, 3) * (2 * maximum_coordinate_value)) - maximum_coordinate_value

    return points


def generate_cube_from_center(point):
    # in order for the cube to be unit
    h = 2

    cube_vertices = np.array((
        (point[0] - h / 2, point[1] - h / 2, point[2] - h / 2),
        (point[0] + h / 2, point[1] - h / 2, point[2] - h / 2),
        (point[0] + h / 2, point[1] + h / 2, point[2] - h / 2),
        (point[0] - h / 2, point[1] + h / 2, point[2] - h / 2),
        (point[0] - h / 2, point[1] - h / 2, point[2] + h / 2),
        (point[0] + h / 2, point[1] - h / 2, point[2] + h / 2),
        (point[0] + h / 2, point[1] + h / 2, point[2] + h / 2),
        (point[0] - h / 2, point[1] + h / 2, point[2] + h / 2),
    ))
    return cube_vertices


def generate_sphere_normal_vector():
    # Φ(θ,ϕ)=(Rsinϕcosθ,Rsinϕsinθ,Rcosϕ)
    r = 1
    theta = np.random.uniform(low=0, high=2 * np.pi)
    phi = np.random.uniform(low=0, high=np.pi)

    return np.array([r * np.cos(theta) * np.sin(phi),
                     r * np.sin(theta) * np.sin(phi),
                     r * np.cos(phi)])


def find_relative_cubicle_overlap(sphere_overlap):
    cubicle_volume = 1
    #cubicle_volume = np.random.rand(0, 1)

    volume_fraction = sphere_overlap / cubicle_volume

    if volume_fraction > 1:
        volume_fraction = 1

    return volume_fraction


def generate_random_sphere():
    radius = np.random.uniform(low=1, high=10)

    normal = generate_sphere_normal_vector()
    sphere_surface_point = (np.random.rand(1, 3) * (2 * 1)) - 1

    center = sphere_surface_point - normal * radius

    return overlap.Sphere(tuple([center[0][0],
                                 center[0][1],
                                 center[0][2]]), radius)


if __name__ == "__main__":
    hexahedra = np.zeros(shape=(NUMBER_OF_CUBES + 1, 8, 3))

    center_point_of_unit_cirle = np.array([0, 0, 0])
    hexahedra[0, :, :] = generate_cube_from_center(center_point_of_unit_cirle)

    random_cube_centers = random_points_generator(NUMBER_OF_CUBES)

    for cube_center_index, cube_center in enumerate(random_cube_centers):
        hexahedra[cube_center_index + 1, :, :] = generate_cube_from_center(cube_center)

    with open('random_cubicle_and_curvatures.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        for test_no in range(int(NUMBER_OF_SAMPLES)):
            u = []

            sphere = generate_random_sphere()

            for hexahedron in hexahedra:
                hex = overlap.Hexahedron(hexahedron)

                u.append(find_relative_cubicle_overlap(overlap.overlap(sphere, hex)))

            row = [u_n for u_n in u]

            curvature = 2 / sphere.radius
            row.append(curvature)

            writer.writerow(row)
