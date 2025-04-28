import os

USE_SCHEMA_BATCH_MODE = os.getenv("USE_SCHEMA_BATCH_MODE", "True").lower() == "true"
# use os.environ["USE_SCHEMA_BATCH_MODE"] = "false"
# before importing this file to switch to interactive mode (making synchronous calls to the OpenAI API)
# when switching between modes in a notebook, restart the kernel to avoid issues

if USE_SCHEMA_BATCH_MODE:
    from tooldantic import ToolBaseModel, OpenAiResponseFormatGenerator

    class CustomSchemaGenerator(OpenAiResponseFormatGenerator):
        is_inlined_refs = False

    class BaseModel(ToolBaseModel):
        _schema_generator = CustomSchemaGenerator

    print("Schema: Batch Mode")
else:
    from pydantic import BaseModel
    print("Schema: Interactive Mode")
# setup end


# Schema Start
from enum import Enum
from typing import Optional, List

# Enums

class RecipeType(Enum):
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    SALAD = "salad"
    DRINK = "drink"

class KitchenUtensil(Enum):
    oven = "oven"
    loaf_pan = "loaf_pan"
    blender = "blender"
    bowl = "bowl"
    electric_mixer = "electric_mixer"
    wire_rack = "wire_rack"
    glass = "glass"
    muffin_pan = "muffin_pan"
    springform_pan = "springform_pan"
    skillet = "skillet"
    pie_shell = "pie_shell"
    aluminum_foil = "aluminum_foil"
    slow_cooker = "slow_cooker"
    baking_dish = "baking_dish"
    serving_platter = "serving_platter"
    whisk = "whisk"
    cheesecloth = "cheesecloth"
    saucepan = "saucepan"
    tube_pan = "tube_pan"
    baking_sheet = "baking_sheet"
    mixing_bowl = "mixing_bowl"

class OvenInstructions(BaseModel):
    preheat_temperature_celcius: int
    time_in_oven_minutes: int

class ExtractedData(BaseModel):
    pretentious_recipy_name: str # string value, self-explanatory
    is_vegan: bool # simple boolean value, self-explanatory
    oven_instructions: Optional[OvenInstructions] # optional field, can be None if not provided
    recipe_type: RecipeType # enum field, can be one of the defined values, most useful
    necessary_utensils: List[KitchenUtensil] # list of enums, can be empty if no utensils are provided