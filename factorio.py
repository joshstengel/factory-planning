# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 21:06:25 2017

@author: joshs
"""
from math import ceil
        

class FactorioObject(object):
    '''
    Any Factorio object, i.e. Iron plate, Copper plate, Iron gear wheel, etc.
    Basic holder for the recipe for each object.
    
    Args:
        name: Name of the object (ideally directly from Factorio)
        quantiy_produced: The number of the object made per crafting operation
        ingredients: A list of tuples containing the required FactorioObjects
                     and required quantity to craft the reference object. Takes
                     the form [(item1, quantity1), (item2, quantity2)]
        production_time: The amount of time it takes to craft the object
    '''
    def __init__(self, name, quantity_produced, ingredients, production_time):
        self.name = name
        self.quantity_produced = quantity_produced
        self.ingredients = ingredients
        self.production_time = production_time
        
        self.is_base = not ingredients
        
    def __repr__(self):
        return "<FactorioObject:\"%s\">" % self.name
    
    def reference_assembly_machine(self):
        machine = FactorioMachine(self)
        return machine
    
    def reference_output_per_minute(self):
        return self.reference_factory().output_per_minute


class FactorioResource(object):
    def __init__(self, product, quantity_per_minute):
        self.product = product
        self.quantity_per_minute = quantity_per_minute
        
    def __repr__(self):
        return "<FactorioResource:\"%s\":%s/minute>" % (self.product.name, self.quantity_per_minute)


class FactorioMachine(object):
    '''
    Assembling Machine from Factorio.
    
    Args:
        product: The FactorioObject the machine creates
        efficiency: A measure of the throttling for the machine. If the machine
                    can create 10 objects per minute but only is required to
                    build 7, then the efficiency would be 0.7
        machine_type: Integer indication of machine type, i.e. Assembling
                      machine 1 (with a crafting speed of 0.5), Assembling 
                      machine 2 (with a crafting speed of 0.75), or Assembling
                      machine 3 (with a crafting speed of 1.25)
    '''
    def __init__(self, product, efficiency=1, machine_type=1):
        self.output_name = product.name
        self.product = product
        if len(self.product.ingredients) > 4:
            machine_type = 3
        elif len(self.product.ingredients) > 2:
            machine_type = 2
        
        if machine_type == 1:
            self.crafting_speed = 0.5
        elif machine_type == 2:
            self.crafting_speed = 0.75
        elif machine_type == 3:
            self.crafting_speed = 1.25
        else:
            raise Exception("Unknown machine type")
            
        self.machine_type = machine_type
        self.efficiency = efficiency
        self.production_time = self.product.production_time / (self.efficiency * self.crafting_speed)
        self.cycles_per_minute = 60. / self.production_time
        self.output_per_minute = self.product.quantity_produced * self.cycles_per_minute
        
    def __repr__(self):
        return "<FactorioMachine(Type%i):\"%s\":%2.1f" % (self.machine_type, self.output_name, self.efficiency*100) + "%>"
    
    def ingredients_per_minute(self):
        all_ingredients = dict()
        
        def get_child_ingredients(parent_ingredient, parent_quantity):
            if parent_ingredient.is_base:
                return []
            else:
                
                sublist = []
                for ingredient, quantity in parent_ingredient.ingredients:
                    sublist.extend([(ingredient, quantity*parent_quantity)])
                    sublist.extend(get_child_ingredients(ingredient, quantity*parent_quantity/ingredient.quantity_produced))
                return sublist
            
            
        for res in self.product.ingredients:
            ingredient, quantity = res
            num_required = quantity * self.output_per_minute
            if ingredient in all_ingredients:
                all_ingredients[ingredient] += num_required
            else:
                all_ingredients[ingredient] = num_required
        return all_ingredients
    
    def required_machines(self):
        for ingredient in self.ingredients_per_minute():
            
    
    def required_machines(self):
        all_machines = dict()
        for res in self.product.ingredients:
            ingredient, quantity = res
            num_required = quantity * self.output_per_minute * self.efficiency * self.crafting_speed
            if ingredient.is_base:
                if ingredient in all_machines:
                    all_machines[ingredient] += num_required
                else:
                    all_machines[ingredient] = num_required
            else:
                theoretical_output = ingredient.reference_output_per_minute()
                factories_required = num_required / theoretical_output
                efficiency = factories_required / ceil(factories_required)
                if ingredient in all_machines:
                    all_machines[ingredient] += num_required
                else:
                    all_machines[ingredient] = num_required
                all_machines.extend([FactorioMachine(ingredient, efficiency) for _i in range(int(ceil(factories_required)))])
        return all_machines
        
        
def main():
    iron_ore = FactorioObject("Iron ore", 1, [], 0)
    iron_plate = FactorioObject("Iron plate", 1, [(iron_ore, 1)], 3.5)
    gear = FactorioObject("Iron gear wheel", 1, [(iron_plate, 2)], 0.5)
    copper_ore = FactorioObject("Copper ore", 1, [], 0)
    copper_plate = FactorioObject("Copper plate", 1, [(copper_ore, 1)], 3.5)
    red_science = FactorioObject("Science pack 1", 1, [(copper_plate, 1), (gear, 1)], 5)
    coal = FactorioObject("Coal", 1, [], 0)
    petroleum = FactorioObject("Petroleum gas", 1, [], 0)
    
    copper_cable = FactorioObject("Copper cable", 2, [(copper_plate, 1)], 0.5)
    green_circuit = FactorioObject("Electronic circuit", 1, [(copper_cable, 3), (iron_plate, 1)], 0.5)
    plastic = FactorioObject("Plastic bar", 2, [(coal, 1), (petroleum, 20)], 1)
    red_circuit = FactorioObject("Advanced circuit", 1, [(copper_cable, 4), (green_circuit, 2), (plastic, 2)], 6)
    
    print(red_science.reference_factory().required_ingredients())