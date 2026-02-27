# Outfit Generator
The project allows to generate outfits based on what you have in your closet, the occassion, and the weather.  


**Course**: PRA2031 - Python Programming Language  

**Semester**: Spring 2026  

**Team Members:** Aida Hebberecht, Zofia Mielech, Zofia Grabowska, Liske Janssen  

## Description
Our project is inspired by the difficult decisions we have to make each morning: which outfit to wear? A problem almost every girl or woman (and some men as well) have to face each day. Nothing that fits together, and then it also depends on where you are going and what the weather is. This project solves this issue! Just fill in the occasion and the date/weather and this outfit generator will create an outfit for you based on the clothing in your closet!

To make it simple enough for us to code, we have set weather conditions, randomly generated for a year. This way, you can fill in a date, and it will connect that to the weather conditions of that date and it will use that to filter your clothes. We also have a few occasions that can be chosen from, with set clothing that is categorized based on these occasions. From the chosen weather/date and occasion, our generator will filter the clothes and generate an outfit, always including a top, bottoms and shoes, sometimes adding layers or accessoires.

## Features
- Feature 1: the outfit generator program creates weather- and occasion-appropriate outfits
- Feature 2: the code is customizable: change clothes files to your own, change or add occasions, weighted randomness (for favorite items)
- Feature 3: you can keep generating random outfits until you get one you want

## Installation
### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/zooomie3/Fashionista.git
cd Fashionista
```
2. Install dependencies:
```bash
pip install pandas Pillow
```

## Usage
### Basic Example
from your_module import YourClass
#Create an instance
obj = YourClass(param1, param2)

#Use it
result = obj.do_something()
print(result)

### Common Use Cases
### Use Case 1: Title
#Example code 
### Use Case 2: Title
#Example code

## Project structure
```text
Fashionista/
├── accessories/       # Image files for accessories
├── bags/              # Image files for bags
├── bottoms/           # Image files for pants/skirts
├── hats/              # Image files for hats
├── layers/            # Image files for layers
├── outside/           # Image files for outwear
├── shoes/             # Image files for shoes
├── tops/              # Image files for shirts
├── main.py            # Main application logic
├── collage.py         # Visualizer and image layout engine
├── random_outfit.py   # Test script for generating random outfits
├── occasion_rules.py  # Dictionary mapping occasions to clothing IDs
├── weather.csv        # Weather data for filtering
└── README.md          # This file
```

## License
This project does not have any licenses.

## Authors
- Aida Hebberecht - aidahebberecht-cloud
- Zofia Mielech - zooomie3
- Zofia Grabowska - sli-mak
- Liske Janssen - LiskeJ

## Credits
- Aida Hebberecht: 
- Zofia Mielech: 
- Zofia Grabowska: 
- Liske Janssen: Created the occasion rules: a dictionary with the occasions and the corresponding clothing id's, and coded the logic of weather conditions: when outerwear is needed or excluded, sunglasses and rain clothing.

## Acknowledgments
- Special thanks to [Mentor/Teacher]

Last Updated: February 2026
