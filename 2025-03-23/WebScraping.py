from bs4 import BeautifulSoup
import requests
import pandas as pd

website = "https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700"

def collect_page_data(url):
    result = requests.get(url)
    content = result.text
    
    soup = BeautifulSoup(content, 'html.parser')
    
    main_content = soup.find(class_='ssrcss-1xwx0nq-Grid e1p7pssy1')
    title = main_content.find('h1').get_text()
    
    rating_div = soup.find('div', {'data-testid': 'recipe-rating'})
    rating_value = None
    rating_count = None
    if rating_div:
        rating_text = rating_div.get_text(strip=True)
        if 'An average of' in rating_text:
            rating_value = rating_text.split('An average of')[1].split('out')[0].strip()
        if 'from' in rating_text:
            rating_count = rating_text.split('from')[1].strip().split(' ')[0]
    
    timing = soup.find(class_="ssrcss-160xqny-Wrapper e85aajs0")
    time = timing.find('dd').get_text() if timing else None
    
    img = soup.find("img")
    img_url = img["src"] if img and "src" in img.attrs else None
    
    ingredients_list = main_content.find('ul')
    ingredients = ingredients_list.get_text() if ingredients_list else None
    
    found_words = ("Dairy-free", "Vegan", "Egg-free", "Healthy", "Vegetarian", "Pregnancy-friendly", "Nut-free")
    
    url_tag = soup.find("meta", property="og:url")
    recipe_url = url_tag["content"] if url_tag and "content" in url_tag.attrs else None
    
    data = {
        "Title": title,
        "Rating Value": rating_value,
        "Rating Count": rating_count,
        "Time": time,
        "Image URL": img_url,
        "Ingredients": ingredients,
        "Dietary Info": ', '.join(found_words),
        "URL": recipe_url
    }
    
    df = pd.DataFrame([data])
    df.to_csv("reciperevised.csv", index=False)
    
    print("Data saved to 'reciperevised.csv'.")

collect_page_data(website)
