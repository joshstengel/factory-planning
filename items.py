# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 18:32:39 2017

@author: joshs
"""
from factorio import *

iron_ore = FactorioBaseResource("Iron ore")
iron_plate = FactorioSmeltedResource("Iron plate", [(iron_ore, 1)], 3.5)
gear = FactorioObject("Iron gear wheel", 1, [(iron_plate, 2)], 0.5)

copper_ore = FactorioBaseResource("Copper ore")
copper_plate = FactorioSmeltedResource("Copper plate", [(copper_ore, 1)], 3.5)
red_science = FactorioObject("Science pack 1", 1, [(copper_plate, 1), (gear, 1)], 5)

coal = FactorioBaseResource("Coal")
petroleum = FactorioBaseResource("Petroleum gas")
copper_cable = FactorioObject("Copper cable", 2, [(copper_plate, 1)], 0.5)
green_circuit = FactorioObject("Electronic circuit", 1, [(copper_cable, 3), (iron_plate, 1)], 0.5)
plastic = FactorioObject("Plastic bar", 2, [(coal, 1), (petroleum, 20)], 1, machine_type=3)
red_circuit = FactorioObject("Advanced circuit", 1, [(copper_cable, 4), (green_circuit, 2), (plastic, 2)], 6)
sulfuric_acid = FactorioBaseResource("Sulfuric acid")
blue_circuit = FactorioObject("Processing unit", 1, [(red_circuit, 2), (green_circuit, 20), (sulfuric_acid, 5)], 10)