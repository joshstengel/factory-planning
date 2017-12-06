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

BATTERY = FactorioObject("Battery", 1, [(COPPER_PLATE, 1), (IRON_PLATE, 1), (SULFURIC_ACID, 20)], 5)
SPEED_MODULE_1 = FactorioObject("Speed module", 1, [(RED_CIRCUIT, 5), (GREEN_CIRCUIT, 5)], 15)
YELLOW_SCIENCE = FactorioObject("High tech science pack", 
                                2, 
                                [(BATTERY, 1), 
                                 (COPPER_CABLE, 30), 
                                 (BLUE_CIRCUIT, 3), 
                                 (SPEED_MODULE_1, 1)], 
                                14)

INSERTER = FactorioObject("Inserter", 1, [(GREEN_CIRCUIT, 1), (GEAR, 1), (IRON_PLATE, 1)], 0.5)
TRANSPORT_BELT = FactorioObject("Transport belt", 2, [(GEAR, 1), (IRON_PLATE, 1)], 0.5)
GREEN_SCIENCE = FactorioObject("Science pack 2", 1, [(INSERTER, 1), (TRANSPORT_BELT, 1)], 6)

ELECTRIC_MINE = FactorioObject("Electric mining drill", 1, [(GREEN_CIRCUIT, 3), (GEAR, 5), (IRON_PLATE, 10)], 2)
PIPE = FactorioObject("Pipe", 1, [(IRON_PLATE, 1)], 0.5)
STEEL = FactorioSmeltedResource("Steel plate", [(IRON_PLATE, 5)], 17.5)
ENGINE = FactorioObject("Engine unit", 1, [(GEAR, 1), (PIPE, 2), (STEEL, 1)], 10)
BLUE_SCIENCE = FactorioObject("Science pack 3", 1, [(RED_CIRCUIT, 1), (ELECTRIC_MINE, 1), (ENGINE, 1)], 12)

GRENADE = FactorioObject("Grenade", 1, [(COAL, 10), (IRON_PLATE, 5)], 8)
GUN_TURRET = FactorioObject("Gun turret", 1, [(COPPER_PLATE, 10), (GEAR, 10), (IRON_PLATE, 20)], 8)
YELLOW_AMMO = FactorioObject("Firearm magazine", 1, [(IRON_PLATE, 4)], 1)
RED_AMMO = FactorioObject("Piercing rounds magazine", 1, [(COPPER_PLATE, 5), (YELLOW_AMMO, 1), (STEEL, 1)], 3)
GRAY_SCIENCE = FactorioObject("Military science pack", 2, [(GRENADE, 1), (GUN_TURRET, 1), (RED_AMMO, 1)], 10)

ASSEMBLING_MACHINE = FactorioObject("Assembling machine 1", 1, [(GREEN_CIRCUIT, 3), (GEAR, 5), (IRON_PLATE, 9)], 0.5)
LUBRICANT = FactorioBaseResource("Lubricant")
ELECTRIC_ENGINE = FactorioObject("Electric engine unit", 1, [(GREEN_CIRCUIT, 2), (ENGINE, 1), (LUBRICANT, 15)], 10)
STONE = FactorioBaseResource("Stone")
STONE_BRICK = FactorioSmeltedResource("Stone brick", [(STONE, 2)], 3.5)
ELECTRIC_FURNACE = FactorioObject("Electric furnace", 1, [(RED_CIRCUIT, 5), (STEEL, 10), (STONE_BRICK, 1)], 3.5)
PURPLE_SCIENCE = FactorioObject("Production science pack", 
                                2, 
                                [(ASSEMBLING_MACHINE, 1), 
                                 (ELECTRIC_ENGINE, 1), 
                                 (ELECTRIC_FURNACE, 1)], 
                                14)