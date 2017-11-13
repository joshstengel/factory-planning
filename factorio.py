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
        return "<FactorioObject:\"{name}\">".format(name=self.name)
    
    def reference_assembling_machine(self):
        '''
        The cheapest Assembling machine that would build this object, running
        at full capacity.
        '''
        machine = FactorioMachine(self)
        return machine
    
    def reference_output_per_minute(self):
        '''
        The maximum output per minute possible for this object using the 
        reference_assembling_machine.
        '''
        return self.reference_assembling_machine().output_per_minute


class FactorioResource(object):
    '''
    Not currently used. Maybe won't ever be used. But I had plans. Oh, how I 
    had plans.
    '''
    def __init__(self, product, quantity_per_minute):
        self.product = product
        self.quantity_per_minute = quantity_per_minute
        
    def __repr__(self):
        return "<FactorioResource:\"{name}\":{qpm}/minute>".format(name=self.product.name, qpm=self.quantity_per_minute)


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
        '''
        This is probably the wrong way to do this but it is convenient. Shows
        the important information for this machine: machine_type (i.e. 
        Assembling machine 1, Assembling machine 2, etc.), the product of the
        machine, and the efficiency. 
        '''
        return "<FactorioMachine(Type{mtype}):\"{out_name}\":{eff_pct:0.2f}%>".format(mtype=self.machine_type, 
                                                                                      out_name=self.output_name,
                                                                                      eff_pct=self.efficiency*100)
    
    def ingredients_per_minute(self):
        '''
        Returns the total number of each ingredient needed per minute. This is
        different than the "total raw" values shown in game in that this one is
        focused on how many Assembling machines would be required. So if an
        item needs Iron gear wheels, this method would return Iron gear wheels,
        Iron plates, and Iron ore.
        '''
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
            
        all_ingredients = get_child_ingredients(self.product, self.output_per_minute)
        
        ingredient_dict = {}
        for ingredient, quantity in all_ingredients:
            if ingredient in ingredient_dict:
                ingredient_dict[ingredient] += quantity
            else:
                ingredient_dict[ingredient] = quantity
        return ingredient_dict
    
    def required_assembling_machines(self):
        '''
        Returns the number of feeder assembling machines needed to drive this
        assembling machine at full capacity. This assumes each feeder machine
        is the cheapest Assembling machine necessary to build the object.
        '''
        all_machines = []
        all_ingredients = self.ingredients_per_minute()
        for ingredient in all_ingredients:
            if ingredient.is_base:
                continue
            quantity = all_ingredients[ingredient]
            ratio = quantity / ingredient.reference_output_per_minute()
            factories = ceil(ratio)
            efficiency = ratio / factories
            all_machines.append(FactorioMachine(ingredient, efficiency))
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
    
    print(red_circuit.reference_assembling_machine().required_assembling_machines())