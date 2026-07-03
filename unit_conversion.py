import pandas as pd

recipes_df = pd.read_json('panelinha_dessert_recipes.json')
print(recipes_df.shape)