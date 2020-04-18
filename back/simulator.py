import json
from typing import Dict, Any, List

import numpy as np


G = 6.67430*10**-11


def get_rang_string(num_letter=2, num_digits=3):
    letters = 'abcdefghjklmnopqrstuvwxyz'
    digits = '0123456789'
    return "".join(np.random.choice(letters, num_letter)) + "".join(np.random.choice(digits, num_digits))


class Body:
    def __init__(self, obj: Dict[str, Any]):
        self._name = obj['name'] if 'name' in obj.keys() else get_rang_string()
        self._mass = obj['mass']
        self._speed = np.array(obj['speed'])
        self._radius = obj['radius']
        self._coordinate = np.array(obj['coordinate'])
        self._force = np.zeros_like(self._coordinate)

    def get_coordinate(self):
        return self._coordinate

    def get_mass(self) -> float:
        return self._mass

    def add_force(self, force):
        self._force = force

    def get_state(self) -> Dict[str, Any]:
        return {
            'name': self._name,
            'mass': self._mass,
            'radius': self._radius,
            'coordinate': self._coordinate,
            'speed': self._speed,
        }

    def step(self, dt: float):
        self._coordinate += self._speed * dt
        self._speed += self._force * dt


def dist(a: Body, b: Body) -> float:
    return ((a.get_coordinate() - b.get_coordinate())**2).sum()


def get_force_module(a: Body, b: Body) -> float:
    return G * a.get_mass() * b.get_mass() / dist(a, b)**2


def vector_len(vector) -> float:
    return (vector**2).sum()


def get_unit_vector_A2B(a: Body, b: Body):
    if a.get_coordinate() == b.get_coordinate():
        return np.zeros_like(a.get_coordinate())
    vector = b.get_coordinate() - a.get_coordinate()
    return vector / vector_len(vector)


def get_force_A2B(a: Body, b: Body):
    unit_vector = get_unit_vector_A2B(a, b)
    return unit_vector * get_force_module(a, b)


class Simulator:
    def __init__(self, settings_file_path):
        self._obj_list: List[Body] = []
        self._settings = {}
        self.load_from_file(settings_file_path)
        self._cur_state = {}
        self._time = 0

    def load_from_file(self, file_path):
        self._obj_list = []
        self._settings = json.load(open(file_path, 'r'))
        self._time = self._settings['start_time'] if 'start_time' in self._settings else 0
        obj_list = self._settings['objects']
        for item in obj_list:
            self._obj_list.append(Body(item))

    def step(self, dt: float):
        for index, obj in self._obj_list:
            force_vector = np.zeros_like(obj.get_coordinates())
            for index2, obj2 in self._obj_list:
                if index == index2:
                    continue
                force_vector += get_force_A2B(obj2, obj)
            obj.add_force(force_vector)

        for obj in self._obj_list:
            obj.step(dt)

    def update_state(self):
        self._cur_state = {
            'objects': [
                x.get_state() for x in self._obj_list
            ],
            'steps': self._time,
            'time': self._time * self._settings['delta_time_per_step'],
        }

    def simulate(self):
        while True:
            self.step(self._settings['delta_time_per_step'])
            self._time += 1
            if self._time % self._settings['update_state_every_N_step']:
                self.update_state()

    def get_state(self) -> Dict[str, Any]:
        return self._cur_state

