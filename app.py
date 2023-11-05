from flask import Flask, request, render_template
from PIL import Image, ImageFilter
from pprint import PrettyPrinter
from dotenv import load_dotenv
import json
import os
import random
import requests

load_dotenv()


app = Flask(__name__)

@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

################################################################################
# COMPLIMENTS ROUTES
################################################################################

list_of_compliments = [
    'awesome',
    'beatific',
    'blithesome',
    'conscientious',
    'coruscant',
    'erudite',
    'exquisite',
    'fabulous',
    'fantastic',
    'gorgeous',
    'indubitable',
    'ineffable',
    'magnificent',
    'outstanding',
    'propitioius',
    'remarkable',
    'spectacular',
    'splendiferous',
    'stupendous',
    'super',
    'upbeat',
    'wondrous',
    'zoetic'
]

@app.route('/compliments')
def compliments():
    """Shows the user a form to get compliments."""
    return render_template('compliments_form.html')

@app.route('/compliments_results')
def compliments_results():
    """Show the user some compliments."""
    
    # get form values:
    users_name = request.args.get('users_name')
    wants_compliments = request.args.get('wants_compliments')
    num_compliments = int(request.args.get('num_compliments'))
    # get n number of compliments
    user_compliments = random.sample(list_of_compliments, num_compliments)
    
    # populate context
    context = {
        'users_name': users_name,
        'wants_compliments': wants_compliments,
        'user_compliments': user_compliments
    }

    return render_template('compliments_results.html', **context)


################################################################################
# ANIMAL FACTS ROUTE
################################################################################

animal_to_fact = {
    'koala': {'habitat': 'Koalas are native to Australia and are primarily found in eucalyptus forests and woodlands. They spend most of their time in the trees.',
              'physical_characteristics': 'Koalas are marsupials and have a unique diet of eucalyptus leaves. They have a specialized digestive system adapted to this diet.',
              'intelligence': 'Koalas have a relatively simple brain structure and are not known for their high intelligence. They rely on instinctual behaviors for survival.'},
    'parrot': {'habitat': 'Parrots are found in a wide range of habitats, including tropical rainforests, deserts, and coastal regions. They are known for their adaptability.',
              'physical_characteristics': 'Parrots are known for their colorful plumage and strong, curved beaks, which they use for cracking nuts and seeds.',
              'intelligence': 'Parrots are highly intelligent birds. They are known for their ability to mimic human speech and solve complex puzzles.'},
    'mantis shrimp': {'habitat': 'Mantis shrimp are marine crustaceans found in shallow tropical and subtropical waters. They are often found in burrows in the seabed.',
              'physical_characteristics': 'Mantis shrimp have highly developed appendages with powerful claws that they use to strike their prey with incredible speed and force.',
              'intelligence': 'Mantis shrimp are not known for their intelligence in the same way that mammals are, but they have remarkable visual capabilities and hunting strategies.',},
    'lion': {'habitat': 'Lions are native to Africa and can be found in various habitats, including savannas, grasslands, and open woodlands. They are social animals that live in prides.',
              'physical_characteristics': 'Lions are known for their muscular bodies, manes (in males), and sharp teeth. They are apex predators in their ecosystems.',
              'intelligence': 'Lions are highly social animals with complex behaviors. They have a well-developed hunting strategy and work together in coordinated group hunts.',},
    'narwhal': {'habitat': 'Narwhals inhabit the Arctic waters of the North Atlantic and the North Pacific. They are often associated with sea ice and cold, deep oceans.',
              'physical_characteristics': 'Narwhals are known for their long spiral tusks, which are actually elongated teeth. These tusks can grow up to 10 feet in length.',
              'intelligence': 'Narwhals are not extensively studied, but they exhibit complex behaviors and are adapted to their challenging Arctic environment.'},
    'whale shark': {'habitat': 'Whale sharks are found in warm, tropical waters around the world. They are known for their seasonal migrations and are often spotted near coral reefs.',
              'physical_characteristics': 'Whale sharks are the largest fish in the ocean, with a distinctive pattern of white spots on their dark blue-gray skin.',
              'intelligence': 'Whale sharks are not considered highly intelligent; they are filter feeders, primarily driven by instinct and their need for food.'}
}

@app.route('/animal_facts')
def animal_facts():
    """Show a form to choose an animal and receive facts."""

    # get form values:
    animals_to_display = request.args.getlist('animal')
    fact_category = request.args.get('fact_category')
    
    # populate context
    context = {
        'animal_to_fact': animal_to_fact,
        'animal_list': animal_to_fact.keys(),
        'animals_to_display': animals_to_display,
        'fact_category': fact_category
    }

    # print(animal)
    return render_template('animal_facts.html', **context)


################################################################################
# IMAGE FILTER ROUTE
################################################################################

filter_types_dict = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR,
    'detail': ImageFilter.DETAIL,
    'edge enhance': ImageFilter.EDGE_ENHANCE,
    'emboss': ImageFilter.EMBOSS,
    'sharpen': ImageFilter.SHARPEN,
    'smooth': ImageFilter.SMOOTH
}

def save_image(image, filter_type):
    """Save the image, then return the full file path of the saved image."""
    # Append the filter type at the beginning (in case the user wants to 
    # apply multiple filters to 1 image, there won't be a name conflict)
    new_file_name = f"{filter_type}-{image.filename}"
    image.filename = new_file_name

    # Construct full file path
    file_path = os.path.join(app.root_path, 'static/images', new_file_name)
    
    # Save the image
    image.save(file_path)

    return file_path


def apply_filter(file_path, filter_name):
    """Apply a Pillow filter to a saved image."""
    i = Image.open(file_path)
    i.thumbnail((500, 500))
    i = i.filter(filter_types_dict.get(filter_name))
    i.save(file_path)

@app.route('/image_filter', methods=['GET', 'POST'])
def image_filter():
    """Filter an image uploaded by the user, using the Pillow library."""
    filter_types = filter_types_dict.keys()

    if request.method == 'POST':
        
        # TODO: Get the user's chosen filter type (whichever one they chose in the form) and save
        # as a variable
        # HINT: remember that we're working with a POST route here so which requests function would you use?
        filter_type = ''
        
        # Get the image file submitted by the user
        image = request.files.get('users_image')

        # TODO: call `save_image()` on the image & the user's chosen filter type, save the returned
        # value as the new file path

        # TODO: Call `apply_filter()` on the file path & filter type

        image_url = f'./static/images/{image.filename}'

        context = {
            # TODO: Add context variables here for:
            # - The full list of filter types
            # - The image URL
        }

        return render_template('image_filter.html', **context)

    else: # if it's a GET request
        context = {
            # TODO: Add context variable here for the full list of filter types
        }
        return render_template('image_filter.html', **context)


################################################################################
# GIF SEARCH ROUTE
################################################################################

"""You'll be using the Tenor API for this next section. 
Be sure to take a look at their API. 

https://tenor.com/gifapi/documentation

Register and make an API key for yourself. 
Set up dotenv, create a .env file and define a variable 
API_KEY with a value that is the api key for your account. """

API_KEY = os.getenv('API_KEY')
print(API_KEY)

TENOR_URL = 'https://api.tenor.com/v1/search'
pp = PrettyPrinter(indent=4)

@app.route('/gif_search', methods=['GET', 'POST'])
def gif_search():
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""
    if request.method == 'POST':
        # TODO: Get the search query & number of GIFs requested by the user, store each as a 
        # variable

        response = requests.get(
            TENOR_URL,
            {
                # TODO: Add in key-value pairs for:
                # - 'q': the search query
                # - 'key': the API key (defined above)
                # - 'limit': the number of GIFs requested
            })

        gifs = json.loads(response.content).get('results')

        context = {
            'gifs': gifs
        }

         # Uncomment me to see the result JSON!
        # Look closely at the response! It's a list
        # list of data. The media property contains a 
        # list of media objects. Get the gif and use it's 
        # url in your template to display the gif. 
        # pp.pprint(gifs)

        return render_template('gif_search.html', **context)
    else:
        return render_template('gif_search.html')

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
