from bs4 import BeautifulSoup
import requests
import pandas as pd

# this is the url i am scraping data from
website = "https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700"


def collect_page_data(url):
    # this sends a get request to the url
    result = requests.get(url)
    # this will extract the html content
    content = result.text
    
    # this parses the html contnt using beautifulsoup(bs4)
    soup = BeautifulSoup(content, 'html.parser')
    
    main_content = soup.find(class_='ssrcss-1xwx0nq-Grid e1p7pssy1')
    # this will extract the recipe title in the main content section
    title = main_content.find('h1').get_text()
    
    rating = soup.find('div', {'data-testid': 'recipe-rating'})
    # I initialize variables for rating value and rating count
    rating_value = None
    rating_count = None
    # if a rating is found, extract the rating value and count
    if rating:
        rating_text = rating.get_text(strip=True)
        if 'An average of' in rating_text:
            # extract the numerical rating value from the text
            rating_value = rating_text.split('An average of')[1].split('out')[0].strip()
        if 'from' in rating_text:
            # extract the number of reviews from the text
            rating_count = rating_text.split('from')[1].strip().split(' ')[0]

    # this will find the cooking time section
    timing = soup.find(class_="ssrcss-160xqny-Wrapper e85aajs0")
    # this will extract cooking time if available
    time = timing.find('dd').get_text() if timing else None
    
    img = soup.find("img")
    # this will extract the image URL if available
    img_url = img["src"] if img and "src" in img.attrs else None
    
    # this will extract the ingredients list
    ingredients_list = main_content.find('ul')
    # this will get the ingredients text if available
    ingredients = ingredients_list.get_text() if ingredients_list else None
    
    # I assigned found words to a list of dietary information keywords to check for
    found_words = ("Dairy-free", "Vegan", "Egg-free", "Healthy", "Vegetarian", "Pregnancy-friendly", "Nut-free")
    
    url_tag = soup.find("meta", property="og:url")
    # this will extract the recipe URL from the meta tag
    recipe_url = url_tag["content"] if url_tag and "content" in url_tag.attrs else None
    
    # this stores extracted data in a dictionary called data
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
    
    # I converted dictionary to a pandas DataFrame
    df = pd.DataFrame([data])
    # this will save data to a CSV file
    df.to_csv("reciperevised.csv", index=False)
    
    # this prints a confirmation message
    print("Data saved to 'reciperevised.csv'.")

collect_page_data(website)