from enum import Enum as PyEnum
from sqlalchemy import Enum


# Staging
class BatchStatus(PyEnum):
    pending = "pending"
    validating = "validating"
    passed = "passed"
    failed = "failed"
    promoted = "promoted"

# dishes
class PrimaryCuisine(PyEnum):
    unknown = "unknown"
    american = "american"
    chinese = "chinese"
    french = "french"
    greek = "greek"
    indian = "indian"
    italian = "italian"
    japanese = "japanese"
    korean = "korean"
    mediterranean = "mediterranean"
    mexican = "mexican"
    middle_eastern = "middle_eastern"
    spanish = "spanish"
    thai = "thai"
    turkish = "turkish"
    vietnamese = "vietnamese"


# dishes
class CourseType(PyEnum):
    appetizer = "appetizer"
    main = "main"
    side = "side"
    dessert = "dessert"


# dishes
class DishCategory(PyEnum):
    appetizer_plate = "appetizer_plate"
    baked_dessert = "baked_dessert"
    baked_entree = "baked_entree"
    baked_pasta = "baked_pasta"
    bbq_smoked_entree = "bbq_smoked_entree"
    braised_entree = "braised_entree"
    breakfast_plate = "breakfast_plate"
    burger = "burger"
    burrito = "burrito"
    casserole = "casserole"
    curry_dish = "curry_dish"
    dessert = "dessert"
    dip_spread = "dip_spread"
    dumpling_dish = "dumpling_dish"
    egg_dish = "egg_dish"
    flatbread = "flatbread"
    fried_entree = "fried_entree"
    frozen_dessert = "frozen_dessert"
    grain_bowl = "grain_bowl"
    grilled_entree = "grilled_entree"
    gyro_doner = "gyro_doner"
    hot_dog_sausage = "hot_dog_sausage"
    hot_pot_stew = "hot_pot_stew"
    kebab_skewer = "kebab_skewer"
    noodle_dish = "noodle_dish"
    noodle_soup = "noodle_soup"
    pasta_dish = "pasta_dish"
    pizza = "pizza"
    quesadilla = "quesadilla"
    rice_bowl = "rice_bowl"
    roasted_entree = "roasted_entree"
    salad = "salad"
    sandwich = "sandwich"
    sauce_condiment = "sauce_condiment"
    sauteed_entree = "sauteed_entree"
    savory_pancake = "savory_pancake"
    savory_pastry = "savory_pastry"
    savory_pie_tart = "savory_pie_tart"
    side_dish = "side_dish"
    slider = "slider"
    snack_plate = "snack_plate"
    soup = "soup"
    steamed_entree = "steamed_entree"
    stew = "stew"
    stir_fry = "stir_fry"
    stuffed_flatbread = "stuffed_flatbread"
    stuffed_pasta = "stuffed_pasta"
    sushi = "sushi"
    taco = "taco"
    tapas_meze = "tapas_meze"
    wrap = "wrap"


# dishes
class MealTiming(PyEnum):
    breakfast = "breakfast"
    brunch = "brunch"
    dinner = "dinner"
    late_night = "late_night"
    lunch = "lunch"
    snack = "snack"


class QAStatus(PyEnum):
    draft = "draft"
    needs_review = "needs_review"
    approved = "approved"
    blocked = "blocked"


class DataSource(PyEnum):
    manual_entry = "manual_entry"
    ai_pipeline_v1 = "ai_pipeline_v1"
    import_partner = "import_partner"
    unknown = "unknown"
    
class Severity(PyEnum):
    error = "error"
    warning = "warning"
    
class OverallStatus(PyEnum):
    pass_ = "pass"  # 'pass' is a reserved word in Python so use pass_
    fail = "fail"

# SQLAlchemy Enum type objects bound to the Python enum classes above.
# Use these in mapped_column(...) so enum DDL/type naming is centralized and
# reusable across models.
batch_status_enum = Enum(BatchStatus, name="batch_status_enum")
primary_cuisine_enum = Enum(PrimaryCuisine, name="primary_cuisine_enum")
course_type_enum = Enum(CourseType, name="course_type_enum")
dish_category_enum = Enum(DishCategory, name="dish_category_enum")
meal_timing_enum = Enum(MealTiming, name="meal_timing_enum")
qa_status_enum = Enum(QAStatus, name="qa_status_enum")
data_source_enum = Enum(DataSource, name="data_source_enum")
severity_enum = Enum(Severity, name="severity_enum")
overall_status_enum = Enum(OverallStatus, name="overall_status_enum")
