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
    def __init__(self, name, quantity_produced, ingredients, production_time, machine_type=None):
        self.name = name
        self.quantity_produced = quantity_produced
        self.ingredients = ingredients
        self.production_time = production_time
        self.machine_type = machine_type

    def __repr__(self):
        return "<FactorioObject:\"{name}\">".format(name=self.name)
    
    def reference_machine(self):
        '''
        The cheapest Assembling machine that would build this object, running
        at full capacity.
        '''
        if self.machine_type:
            machine = FactorioMachine(self, machine_type=self.machine_type)
        else:
            machine = FactorioMachine(self)
        return machine
    
    def reference_output_per_minute(self):
        '''
        The maximum output per minute possible for this object using the 
        reference_assembling_machine.
        '''
        return self.reference_machine().output_per_minute


class FactorioBaseResource(object):
    '''
    Holder for mined resources (Iron ore, Copper ore, Stone, Coal, Uranium ore)
    and liquid resources. 
    '''
    def __init__(self, name):
        self.name = name
        self.quantity_produced = 1.
        self.ingredients = []
            
    def __repr__(self):
        return "<FactorioBaseResource:\"{name}\">".format(name=self.name)
    
    def reference_machine(self):
        return
    
    def reference_output_per_minute(self):
        return 


class FactorioSmeltedResource(object):
    '''
    Iron plate, Copper plate, Stone brick, Steel plate
    '''
    def __init__(self, name, ingredients, production_time):
        self.name = name
        if len(ingredients) > 1:
            raise Exception("Should only be a single ingredient")
        self.ingredients = ingredients
        self.production_time = production_time
        
        self.quantity_produced = 1
#        self.is_base = False
        
    def __repr__(self):
        return "<FactorioSmeltedResource:\"{name}\">".format(name=self.name)
        
    def reference_machine(self):
        return FactorioFurnace(self)
    
    def reference_output_per_minute(self):
        return self.reference_machine().output_per_minute
    

class FactorioFurnace(object):
    '''
    Furnace from Factorio.
    
    Args:
        product: The FactorioSmeltedResource the machine creates
        efficiency: A measure of the throttling for the machine. If the machine
                    can create 10 objects per minute but only is required to
                    build 7, then the efficiency would be 0.7
        crafting_speed: Crafting speed of the furnace. Either 1 or 2. Default
                        is 2, which assumes that we are past the point of the
                        stone furnace
    '''
    def __init__(self, product, efficiency=1, crafting_speed=2):
        self.product = product
        self.output_name = product.name
        self.efficiency = efficiency
        self.crafting_speed = crafting_speed
        self.production_time = self.product.production_time / (self.efficiency * self.crafting_speed)
        self.output_per_minute = 60. / self.production_time
        
    def __repr__(self):
        return "<FactorioFurnace:\"{out_name}\":{eff_pct:2.1f}%>".format(out_name=self.output_name,
                                                                         eff_pct=self.efficiency*100)
    
    def ingredient_per_minute(self):
        ingredient, quantity = self.product.ingredients[0]
        rate = self.product.production_time * self.efficiency * self.crafting_speed * quantity
        return {ingredient: rate}


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
        return "<FactorioMachine(Type{mtype}):\"{out_name}\":{eff_pct:2.1f}%>".format(mtype=self.machine_type,
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
            if not parent_ingredient.ingredients:
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
        assembling machine at given capacity. This assumes each feeder machine
        is the cheapest Assembling machine necessary to build the object.
        '''
        all_ingredients = self.ingredients_per_minute()
        return required_assembling_machines(all_ingredients)
    
    def required_furnaces(self):
        '''
        Returns the number of furnaces needed to drive this assembling machine
        at given capacity.
        '''
        all_ingredients = self.ingredients_per_minute()
        return required_furnaces(all_ingredients)


class FactorioMachinePack(object):
    '''
    This is purely a convenient object to have a useful repr that allows me to
    see how many of each machine I actually need
    '''
    def __init__(self, machine, number):
        self.machine = machine
        self.number = number
        
    def __repr__(self):
        return "{num}*{machine}".format(num=self.number,
                                        machine=self.machine.__repr__())
        
    def ingredients_per_minute(self):
        ref = self.machine.ingredients_per_minute
        total = {}
        for ingredient in ref:
            total[ingredient] = self.number * ref[ingredient]
        return total
    
    def required_assembling_machines(self):
        '''
        Returns the number of feeder assembling machines needed to drive the
        machines in this pack at their specified capacities
        '''
        all_ingredients = self.ingredients_per_minute()
        return required_assembling_machines(all_ingredients)
    
    def required_furnaces(self):
        '''
        Returns the number of furnaces needed to drive the machines in this
        pack at their specified capacities
        '''
        all_ingredients = self.ingredients_per_minute()
        return required_furnaces(all_ingredients)


def required_assembling_machines(all_ingredients):
    all_machines = []
    for ingredient in all_ingredients:
        if not isinstance(ingredient, FactorioObject):
            continue
        quantity = all_ingredients[ingredient]
        ratio = quantity / ingredient.reference_output_per_minute()
        factories = ceil(ratio)
        efficiency = ratio / factories
        if ingredient.machine_type:
            pack = FactorioMachinePack(FactorioMachine(ingredient, efficiency, ingredient.machine_type), factories)
        else:
            pack = FactorioMachinePack(FactorioMachine(ingredient, efficiency), factories)
        all_machines.append(pack)
    return all_machines


def required_furnaces(all_ingredients):
    all_furnaces = []
    for ingredient in all_ingredients:
        if not isinstance(ingredient, FactorioSmeltedResource):
            continue
        quantity = all_ingredients[ingredient]
        ratio = quantity / ingredient.reference_output_per_minute()
        furnaces = ceil(ratio)
        efficiency = ratio / furnaces
        pack = FactorioMachinePack(FactorioFurnace(ingredient, efficiency), furnaces)
        all_furnaces.append(pack)
    return all_furnaces

    
if __name__ == '__main__':
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
    print(blue_circuit.reference_machine().required_assembling_machines())
    print(blue_circuit.reference_machine().required_furnaces())
    