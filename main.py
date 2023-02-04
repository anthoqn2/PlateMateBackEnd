from fastapi import FastAPI
import urllib.request
import urllib.parse
import json 

def main():
    #get_Price("Lamb")
    get_Recipes("lamb")

"""def get_Price(item):
    #url = "https://api.kroger.com/v1/products?filter.term={" + item + "}&filter.locationId={01400943}"
    url = "https://api.kroger.com/v1/products?filter.brand=Kroger&filter.term=lamb&filter.locationId=01400943"
    json_file = get_json_file(url)
    d = {"Regular Price": json_file["data"][0]["items"][0]["price"]["regular"]}
    print(d)"""

def get_Saved_Recipe(id):
    url = "https://api.edamam.com/api/recipes/v2/" + id + "?type=public&app_id=6bef399e&app_key=cc4d4b804b9ddc917ba1f15ea28babc4"
    json_file = get_json_file(url)
    d = {"recipe" : json_file["recipe"]["label"], "ingredients" : json_file["recipe"]["ingredientLines"],
        "image" : json_file["recipe"]["image"], "recipe_id": json_file["recipe"]["uri"][json_file["recipe"]["uri"].find("_")+1:]}
    return d
def get_Recipes(search):
    search = search.replace(" ","%20")
    
    url = "https://api.edamam.com/api/recipes/v2?type=public&q=" + search + "&app_id=6bef399e&app_key=cc4d4b804b9ddc917ba1f15ea28babc4"
    recipe_name,recipe_ingredients, recipe_id,recipe_image,count = _create_list(get_json_file(url))
    data = {"list" :[], "Search size":count}
    i = 0   
    while i < count:
        data["list"].append({"recipe" : recipe_name[i], "ingredients": recipe_ingredients[i], "image":recipe_image, "recipe_id":recipe_id[i]})
        i+=1
    return data 
"""
Given a url to the search, return the json_file
"""
def get_json_file(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')
        json_data = json.loads(json_text)
        return json_data
    finally:
        if(response != None):
            response.close()

"""
Given a json_file return the recipe name, ingredients, id and image
"""
def _create_list(json_file):
    recipe_name = []
    recipe_ingredients = []
    recipe_id = []
    recipe_image = []

    count = 0
    for index in range(len(json_file["hits"])):
        recipe = json_file["hits"][index]
        
        if count > 20:
            return [recipe_name,recipe_ingredients,recipe_id,recipe_image,count]
        recipe_name.append(recipe["recipe"]["label"])
        recipe_image.append(recipe["recipe"]["image"])
        recipe_ingredients.append(recipe["recipe"]["ingredientLines"])
        start = recipe["recipe"]["uri"].find("_")
        recipe_id.append(recipe["recipe"]["uri"][start+1:])
        count+=1

    return [recipe_name,recipe_ingredients,recipe_id,recipe_image,count]

app = FastAPI()


@app.get("/")
async def search_Recipe(search):
    return get_Recipes(search)
async def load_Saved_Recipe(id):
    return get_Saved_Recipe(id)