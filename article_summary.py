import nltk
nltk.download('punkt')
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from wand.image import Image
import requests
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
from wand.font import Font

url = "https://arstechnica.com/science/2018/06/first-space-then-auto-now-elon-musk-quietly-tinkers-with-education/"
article = Article(url)
article.download()
article.parse()
print(article.images)

LANGUAGE = "english"
SENTENCES_COUNT = 10

parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)

image_url = 'https://i.imgur.com/YobrZ8r.png'
image_blob = requests.get(image_url)
with Image(blob=image_blob.content) as img:
    print(img.size)
    
dims = (1080, 1920)
ideal_width = dims[0]
ideal_height = dims[1]
ideal_aspect = ideal_width / ideal_height

with Image(blob=image_blob.content) as img:
    size = img.size

width = size[0]
height = size[1]
aspect = width/height
CAPTION = ("For the past four years, this "
           "experimental non-profit school has been quietly "
           "educating Musk’s sons, the children of select "
           "SpaceX employees, and a few high-achievers "
           "from nearby Los Angeles.")

if aspect > ideal_aspect:
    # Then crop the left and right edges:
    new_width = int(ideal_aspect * height)
    offset = (width - new_width) / 2
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(width-new_width), 0, int(width), int(height))
    )
else:
    # ... crop the top and bottom:
    new_height = int(width / ideal_aspect)
    offset = (height - new_height) / 2
    resize = (
        (0, 0, int(width), int(new_height)), 
        (0, int(height-new_height), int(width), int(height))
    )

with Image(blob=image_blob.content) as canvas:
    print(canvas.width)
    canvas.crop(*resize[0])
    print(canvas.width)
    canvas.font = Font("SanFranciscoDisplay-Bold.otf", 
                        size=53, 
                        color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(canvas.height/2)
    canvas.caption(CAPTION, gravity='center', 
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_1.jpg')

with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[1])
    canvas.font = Font("SanFranciscoDisplay-Bold.otf", 
                        size=53, 
                        color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(30)
    canvas.caption(CAPTION, gravity='north', 
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_2.jpg')