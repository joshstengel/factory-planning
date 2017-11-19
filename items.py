# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 18:32:39 2017

@author: joshs
"""
from factorio import *

IRON_ORE = FactorioBaseResource("Iron ore")
IRON_PLATE = FactorioSmeltedResource("Iron plate", [(IRON_ORE, 1)], 3.5)
GEAR = FactorioObject("Iron gear wheel", 1, [(IRON_PLATE, 2)], 0.5)

COPPER_ORE = FactorioBaseResource("Copper ore")
COPPER_PLATE = FactorioSmeltedResource("Copper plate", [(COPPER_ORE, 1)], 3.5)
RED_SCIENCE = FactorioObject("Science pack 1", 1, [(COPPER_PLATE, 1), (GEAR, 1)], 5)

COAL = FactorioBaseResource("Coal")
PETROLEUM = FactorioBaseResource("Petroleum gas")
COPPER_CABLE = FactorioObject("Copper cable", 2, [(COPPER_PLATE, 1)], 0.5)
GREEN_CIRCUIT = FactorioObject("Electronic circuit", 1, [(COPPER_CABLE, 3), (IRON_PLATE, 1)], 0.5)
PLASTIC = FactorioObject("Plastic bar", 2, [(COAL, 1), (PETROLEUM, 20)], 1, machine_type=3)
RED_CIRCUIT = FactorioObject("Advanced circuit", 1, [(COPPER_CABLE, 4), (GREEN_CIRCUIT, 2), (PLASTIC, 2)], 6)
SULFURIC_ACID = FactorioBaseResource("Sulfuric acid")
BLUE_CIRCUIT = FactorioObject("Processing unit", 1, [(RED_CIRCUIT, 2), (GREEN_CIRCUIT, 20), (SULFURIC_ACID, 5)], 10)