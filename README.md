# Outfit Generator
The project allows to generate outfits based on what you have in your closet, the occassion, and the weather.  


**Course**: PRA2031 - Python Programming Language  

**Semester**: Spring 2026  

**Team Members:** Aida Hebberecht, Zofia Mielech, Zofia Grabowska, Liske Janssen  

## Description
Our project is inspired by the difficult decisions we have to make each morning: which outfit to wear? A problem almost every woman (and some men as well) have to face each day. Nothing in your closet that fits together, and then your outfit also depends on where you are going and what the weather is. This project solves this issue! Just fill in the occasion and the weather conditions and this outfit generator will create an outfit for you based on the clothing in your closet!

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
pip install pandas
# on mac:
pip install pandas Pillow
# on windows:
pip install Pillow
```

## Usage

To generate an outfit, run the main program. The system will use the weather data (`weather.csv`) and your chosen occasion (`occasion_rules.py`) to filter your closet and output the perfect visual collage.

Open your terminal and run the main script. Follow any on-screen prompts to input the date and occasion:
```bash
python main.py
```

### Example Usage
Below are screenshots of what your terminal should look like and what the output should be when running/after you have run the program. You can fill in your own date and occasion. In the example, the date is 06-05-2026 and the occasion is night out.

<img width="1261" height="412" alt="image" src="https://github.com/user-attachments/assets/3026fde5-9fbe-40d9-83aa-bdc2111ea264" />

<img width="750" height="1150" alt="image" src="https://github.com/user-attachments/assets/6befcfa4-fda9-44e3-8b0c-9ac728bc1078" />


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
## Project division
If you are working with multiple people, the coding work can be divided.
First, you need to 'create' a closet: import files of clothing and label them: give them an id like "TOP_1".
Besides, weather must be generated, or if licenced, you can use real time weather (but this is more complex)
Then, you need to decide on which clothes fit in which occasion and make a dictionary of this data.
After all the data is ready, the coding can begin.

Then the work can be divided into:
- Data management: loading and cleaning data, handling missing values
- Filtering: the available clothing gets filtered by occasion and temperature
- Outfit logic: making sure the outfit is complete (required items: 1 top, 1 bottoms, 1 shoes), but also has optional items. Makes random selection and adapts required items based on the weather.
- Visualisation: loads the images and creates a collage based on the outfit the generator determined.

Then, all the codes must come together and call on each other so that all the filtering and rules get taken into account for the outfit generator. The separate files can be merged into one.

## License
This project does not have any licenses.

## Authors
- Aida Hebberecht - aidahebberecht-cloud
- Zofia Mielech - zooomie3
- Zofia Grabowska - sli-mak
- Liske Janssen - LiskeJ

## Last updated: March 2026
