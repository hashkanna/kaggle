import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from nltk.stem.snowball import SnowballStemmer
import re

stemmer = SnowballStemmer('english')

df_train = pd.read_csv('../input/train.csv', encoding='ISO-8859-1')
df_test = pd.read_csv('../input/test.csv', encoding='ISO-8859-1')
df_pro_desc = pd.read_csv('../input/product_descriptions.csv')

num_train = df_train.shape[0]


def str_stemmer(s):
    return ' '.join([stemmer.stem(word) for word in s.lower().split()])


def str_common_word(str1, str2):
    return sum(int(str2.find(word)>=0) for word in str1.split())


## This function perfroms spell correction.
## It may take other automatically engineered dictionary as an additional input.
def spell_correction(s, automatic_spell_check_dict={}):
    s = s.replace("craftsm,an","craftsman")
    s = re.sub(r'depot.com/search=', '', s)
    s = re.sub(r'pilers,needlenose', 'pliers, needle nose', s)

    s=s.replace("ttt","tt")
    s=s.replace("lll","ll")
    s=s.replace("nnn","nn")
    s=s.replace("rrr","rr")
    s=s.replace("sss","ss")
    s=s.replace("zzz","zz")
    s=s.replace("ccc","cc")
    s=s.replace("eee","ee")

    s=s.replace("acccessories","accessories")
    s=re.sub(r'\bscott\b', 'scotts', s) #brand
    s=re.sub(r'\borgainzer\b', 'organizer', s)
    s=re.sub(r'\bshark bite\b', 'sharkbite',s)

    s=s.replace("hinges with pishinges with pins","hinges with pins")
    s=s.replace("virtue usa","virtu usa")
    s=re.sub('outdoor(?=[a-rt-z])', 'outdoor ', s)
    s=re.sub(r'\bdim able\b',"dimmable", s)
    s=re.sub(r'\blink able\b',"linkable", s)
    s=re.sub(r'\bm aple\b',"maple", s)
    s=s.replace("aire acondicionado", "air conditioner")
    s=s.replace("borsh in dishwasher", "bosch dishwasher")
    s=re.sub(r'\bapt size\b','appartment size', s)
    s=re.sub(r'\barm[e|o]r max\b','armormax', s)
    s=re.sub(r' ss ',' stainless steel ', s)
    s=re.sub(r'\bmay tag\b','maytag', s)
    s=re.sub(r'\bback blash\b','backsplash', s)
    s=re.sub(r'\bbum boo\b','bamboo', s)
    s=re.sub(r'(?<=[0-9] )but\b','btu', s)
    s=re.sub(r'\bcharbroi l\b','charbroil', s)
    s=re.sub(r'\bair cond[it]*\b','air conditioner', s)
    s=re.sub(r'\bscrew conn\b','screw connector', s)
    s=re.sub(r'\bblack decker\b','black and decker', s)
    s=re.sub(r'\bchristmas din\b','christmas dinosaur', s)
    s=re.sub(r'\bdoug fir\b','douglas fir', s)
    s=re.sub(r'\belephant ear\b','elephant ears', s)
    s=re.sub(r'\bt emp gauge\b','temperature gauge', s)
    s=re.sub(r'\bsika felx\b','sikaflex', s)
    s=re.sub(r'\bsquare d\b', 'squared', s)
    s=re.sub(r'\bbehring\b', 'behr', s)
    s=re.sub(r'\bcam\b', 'camera', s)
    s=re.sub(r'\bjuke box\b', 'jukebox', s)
    s=re.sub(r'\brust o leum\b', 'rust oleum', s)
    s=re.sub(r'\bx mas\b', 'christmas', s)
    s=re.sub(r'\bmeld wen\b', 'jeld wen', s)
    s=re.sub(r'\bg e\b', 'ge', s)
    s=re.sub(r'\bmirr edge\b', 'mirredge', s)
    s=re.sub(r'\bx ontrol\b', 'control', s)
    s=re.sub(r'\boutler s\b', 'outlets', s)
    s=re.sub(r'\bpeep hole', 'peephole', s)
    s=re.sub(r'\bwater pik\b', 'waterpik', s)
    s=re.sub(r'\bwaterpi k\b', 'waterpik', s)
    s=re.sub(r'\bplex[iy] glass\b', 'plexiglass', s)
    s=re.sub(r'\bsheet rock\b', 'sheetrock',s)
    s=re.sub(r'\bgen purp\b', 'general purpose',s)
    s=re.sub(r'\bquicker crete\b', 'quikrete',s)
    s=re.sub(r'\bref ridge\b', 'refrigerator',s)
    s=re.sub(r'\bshark bite\b', 'sharkbite',s)
    s=re.sub(r'\buni door\b', 'unidoor',s)
    s=re.sub(r'\bair tit\b','airtight', s)
    s=re.sub(r'\bde walt\b','dewalt', s)
    s=re.sub(r'\bwaterpi k\b','waterpik', s)
    s=re.sub(r'\bsaw za(ll|w)\b','sawzall', s)
    s=re.sub(r'\blg elec\b', 'lg', s)
    s=re.sub(r'\bhumming bird\b', 'hummingbird', s)
    s=re.sub(r'\bde ice(?=r|\b)', 'deice',s)
    s=re.sub(r'\bliquid nail\b', 'liquid nails', s)
    s=re.sub(r'\bdeck over\b','deckover', s)
    s=re.sub(r'\bcounter sink(?=s|\b)','countersink', s)
    s=re.sub(r'\bpipes line(?=s|\b)','pipeline', s)
    s=re.sub(r'\bbook case(?=s|\b)','bookcase', s)
    s=re.sub(r'\bwalkie talkie\b','2 pair radio', s)
    s=re.sub(r'(?<=^)ks\b', 'kwikset',s)
    s=re.sub('(?<=[0-9])[\ ]*ft(?=[a-z])', 'ft ', s)
    s=re.sub('(?<=[0-9])[\ ]*mm(?=[a-z])', 'mm ', s)
    s=re.sub('(?<=[0-9])[\ ]*cm(?=[a-z])', 'cm ', s)
    s=re.sub('(?<=[0-9])[\ ]*inch(es)*(?=[a-z])', 'in ', s)

    s=re.sub(r'(?<=[1-9]) pac\b', 'pack', s)

    s=re.sub(r'\bcfl bulbs\b', 'cfl light bulbs', s)
    s=re.sub(r' cfl(?=$)', ' cfl light bulb', s)
    s=re.sub(r'candelabra cfl 4 pack', 'candelabra cfl light bulb 4 pack', s)
    s=re.sub(r'\bthhn(?=$|\ [0-9]|\ [a-rtuvx-z])', 'thhn wire', s)
    s=re.sub(r'\bplay ground\b', 'playground',s)
    s=re.sub(r'\bemt\b', 'emt electrical metallic tube',s)
    s=re.sub(r'\boutdoor dining se\b', 'outdoor dining set',s)


    if "a/c" in s:
        if ('unit' in s) or ('frost' in s) or ('duct' in s) or ('filt' in s) or ('vent' in s) or ('clean' in s) or ('vent' in s) or ('portab' in s):
            s=s.replace("a/c","air conditioner")
        else:
            s=s.replace("a/c","ac")


    external_data_dict={'airvents': 'air vents',
    'antivibration': 'anti vibration',
    'autofeeder': 'auto feeder',
    'backbrace': 'back brace',
    'behroil': 'behr oil',
    'behrwooden': 'behr wooden',
    'brownswitch': 'brown switch',
    'byefold': 'bifold',
    'canapu': 'canopy',
    'cleanerakline': 'cleaner alkaline',
    'colared': 'colored',
    'comercialcarpet': 'commercial carpet',
    'dcon': 'd con',
    'doorsmoocher': 'door smoocher',
    'dreme': 'dremel',
    'ecobulb': 'eco bulb',
    'fantdoors': 'fan doors',
    'gallondrywall': 'gallon drywall',
    'geotextile': 'geo textile',
    'hallodoor': 'hallo door',
    'heatgasget': 'heat gasket',
    'ilumination': 'illumination',
    'insol': 'insulation',
    'instock': 'in stock',
    'joisthangers': 'joist hangers',
    'kalkey': 'kelkay',
    'kohlerdrop': 'kohler drop',
    'kti': 'kit',
    'laminet': 'laminate',
    'mandoors': 'main doors',
    'mountspacesaver': 'mount space saver',
    'reffridge': 'refrigerator',
    'refrig': 'refrigerator',
    'reliabilt': 'reliability',
    'replaclacemt': 'replacement',
    'searchgalvanized': 'search galvanized',
    'seedeater': 'seed eater',
    'showerstorage': 'shower storage',
    'straitline': 'straight line',
    'subpumps': 'sub pumps',
    'thromastate': 'thermostat',
    'topsealer': 'top sealer',
    'underlay': 'underlayment',
    'vdk': 'bdk',
    'wallprimer': 'wall primer',
    'weedbgon': 'weed b gon',
    'weedeaters': 'weed eaters',
    'weedwacker': 'weed wacker',
    'wesleyspruce': 'wesley spruce',
    'worklite': 'work light'}

    for word in external_data_dict.keys():
        s=re.sub(r'\b'+word+r'\b',external_data_dict[word], s)

    ############ replace words from dict
    for word in automatic_spell_check_dict.keys():
        s=re.sub(r'\b'+word+r'\b',automatic_spell_check_dict[word], s)

    return s

##### end of dunction 'spell_correction'
############################################


### another replacement dict used independently
another_replacement_dict={"undercabinet": "under cabinet",
"snowerblower": "snower blower",
"mountreading": "mount reading",
"zeroturn": "zero turn",
"stemcartridge": "stem cartridge",
"greecianmarble": "greecian marble",
"outdoorfurniture": "outdoor furniture",
"outdoorlounge": "outdoor lounge",
"heaterconditioner": "heater conditioner",
"heater/conditioner": "heater conditioner",
"conditioner/heater": "conditioner heater",
"airconditioner": "air conditioner",
"snowbl": "snow bl",
"plexigla": "plexi gla",
"whirlpoolga": "whirlpool ga",
"whirlpoolstainless": "whirlpool stainless",
"sedgehamm": "sledge hamm",
"childproof": "child proof",
"flatbraces": "flat braces",
"zmax": "z max",
"gal vanized": "galvanized",
"battery powere weedeater": "battery power weed eater",
"shark bite": "sharkbite",
"rigid saw": "ridgid saw",
"black decke": "black and decker",
"exteriorpaint": "exterior paint",
"fuelpellets": "fuel pellet",
"cabinetwithouttops": "cabinet without tops",
"castiron": "cast iron",
"pfistersaxton": "pfister saxton ",
"splitbolt": "split bolt",
"soundfroofing": "sound froofing",
"cornershower": "corner shower",
"stronglus": "strong lus",
"shopvac": "shop vac",
"shoplight": "shop light",
"airconditioner": "air conditioner",
"whirlpoolga": "whirlpool ga",
"whirlpoolstainless": "whirlpool stainless",
"snowblower": "snow blower",
"plexigla": "plexi gla",
"trashcan": "trash can",
"mountspacesaver": "mount space saver",
"undercounter": "under counter",
"stairtreads": "stair tread",
"techni soil": "technisoil",
"in sulated": "insulated",
"closet maid": "closetmaid",
"we mo": "wemo",
"weather tech": "weathertech",
"weather vane": "weathervane",
"versa tube": "versatube",
"versa bond": "versabond",
"in termatic": "intermatic",
"therma cell": "thermacell",
"tuff screen": "tuffscreen",
"sani flo": "saniflo",
"timber lok": "timberlok",
"thresh hold": "threshold",
"yardguard": "yardgard",
"incyh": "in.",
"diswasher": "dishwasher",
"closetmade": "closetmaid",
"repir": "repair",
"handycap": "handicap",
"toliet": "toilet",
"conditionar": "conditioner",
"aircondition": "air conditioner",
"aircondiioner": "air conditioner",
"comercialcarpet": "commercial carpet",
"commercail": "commercial",
"inyl": "vinyl",
"vinal": "vinyl",
"vynal": "vinyl",
"vynik": "vinyl",
"skill": "skil",
"whirpool": "whirlpool",
"glaciar": "glacier",
"glacie": "glacier",
"rheum": "rheem",
"one+": "1",
"toll": "tool",
"ceadar": "cedar",
"shelv": "shelf",
"toillet": "toilet",
"toiet": "toilet",
"toilest": "toilet",
"toitet": "toilet",
"ktoilet": "toilet",
"tiolet": "toilet",
"tolet": "toilet",
"eater": "heater",
"robi": "ryobi",
"robyi": "ryobi",
"roybi": "ryobi",
"rayobi": "ryobi",
"riobi": "ryobi",
"screww": "screw",
"stailess": "stainless",
"dor": "door",
"vaccuum": "vacuum",
"vacum": "vacuum",
"vaccum": "vacuum",
"vinal": "vinyl",
"vynal": "vinyl",
"vinli": "vinyl",
"viyl": "vinyl",
"vynil": "vinyl",
"vlave": "valve",
"vlve": "valve",
"walll": "wall",
"steal": "steel",
"stell": "steel",
"pcv": "pvc",
"blub": "bulb",
"ligt": "light",
"bateri": "battery",
"kolher": "kohler",
"fame": "frame",
"have": "haven",
"acccessori": "accessory",
"accecori": "accessory",
"accesnt": "accessory",
"accesor": "accessory",
"accesori": "accessory",
"accesorio": "accessory",
"accessori": "accessory",
"repac": "replacement",
"repalc": "replacement",
"repar": "repair",
"repir": "repair",
"replacemet": "replacement",
"replacemetn": "replacement",
"replacemtn": "replacement",
"replaclacemt": "replacement",
"replament": "replacement",
"toliet": "toilet",
"skill": "skil",
"whirpool": "whirlpool",
"stailess": "stainless",
"stainlss": "stainless",
"stainstess": "stainless",
"jigsaww": "jig saw",
"woodwen": "wood",
"pywood": "plywood",
"woodebn": "wood",
"repellant": "repellent",
"concret": "concrete",
"windos": "window",
"wndows": "window",
"wndow": "window",
"winow": "window",
"caamera": "camera",
"sitch": "switch",
"doort": "door",
"coller": "cooler",
"flasheing": "flashing",
"wiga": "wigan",
"bathroon": "bath room",
"sinl": "sink",
"melimine": "melamine",
"inyrtior": "interior",
"tilw": "tile",
"wheelbarow": "wheelbarrow",
"pedistal": "pedestal",
"submerciable": "submercible",
"weldn": "weld",
"contaner": "container",
"webmo": "wemo",
"genis": "genesis",
"waxhers": "washer",
"softners": "softener",
"sofn": "softener",
"connecter": "connector",
"heather": "heater",
"heatere": "heater",
"electic": "electric",
"quarteround": "quarter round",
"bprder": "border",
"pannels": "panel",
"framelessmirror": "frameless mirror",
"paneling": "panel",
"controle": "control",
"flurescent": "fluorescent",
"flourescent": "fluorescent",
"molding": "moulding",
"lattiace": "lattice",
"barackets": "bracket",
"vintemp": "vinotemp",
"vetical": "vertical",
"verticle": "vertical",
"vesel": "vessel",
"versatiube": "versatube",
"versabon": "versabond",
"dampr": "damper",
"vegtable": "vegetable",
"plannter": "planter",
"fictures": "fixture",
"mirros": "mirror",
"topped": "top",
"preventor": "breaker",
"traiter": "trailer",
"ureka": "eureka",
"uplihght": "uplight",
"upholstry": "upholstery",
"untique": "antique",
"unsulation": "insulation",
"unfinushed": "unfinished",
"verathane": "varathane",
"ventenatural": "vent natural",
"shoer": "shower",
"floorong": "flooring",
"tsnkless": "tankless",
"tresers": "dresers",
"treate": "treated",
"transparant": "transparent",
"transormations": "transformation",
"mast5er": "master",
"anity": "vanity",
"tomostat": "thermostat",
"thromastate": "thermostat",
"kphler": "kohler",
"tji": "tpi",
"cuter": "cutter",
"medalions": "medallion",
"tourches": "torch",
"tighrner": "tightener",
"thewall": "the wall",
"thru": "through",
"wayy": "way",
"temping": "tamping",
"outsde": "outdoor",
"bulbsu": "bulb",
"ligh": "light",
"swivrl": "swivel",
"switchplate": "switch plate",
"swiss+tech": "swiss tech",
"sweenys": "sweeney",
"susbenders": "suspender",
"cucbi": "cu",
"gaqs": "gas",
"structered": "structured",
"knops": "knob",
"adopter": "adapter",
"patr": "part",
"storeage": "storage",
"venner": "veneer",
"veneerstone": "veneer stone",
"stm": "stem",
"steqamers": "steamer",
"latter": "ladder",
"steele": "steel",
"builco": "bilco",
"panals": "panel",
"grasa": "grass",
"unners": "runner",
"maogani": "maogany",
"sinl": "sink",
"grat": "grate",
"showerheards": "shower head",
"spunge": "sponge",
"conroller": "controller",
"cleanerm": "cleaner",
"preiumer": "primer",
"fertillzer": "fertilzer",
"spectrazide": "spectracide",
"spaonges": "sponge",
"stoage": "storage",
"sower": "shower",
"solor": "solar",
"sodering": "solder",
"powerd": "powered",
"lmapy": "lamp",
"naturlas": "natural",
"sodpstone": "soapstone",
"punp": "pump",
"blowerr": "blower",
"medicn": "medicine",
"slidein": "slide",
"sjhelf": "shelf",
"oard": "board",
"singel": "single",
"paintr": "paint",
"silocoln": "silicon",
"poinsetia": "poinsettia",
"sammples": "sample",
"sidelits": "sidelight",
"nitch": "niche",
"pendent": "pendant",
"shopac": "shop vac",
"shoipping": "shopping",
"shelfa": "shelf",
"cabi": "cabinet",
"nails18": "nail",
"dewaqlt": "dewalt",
"barreir": "barrier",
"ilumination": "illumination",
"mortice": "mortise",
"lumes": "lumen",
"blakck": "black",
"exterieur": "exterior",
"expsnsion": "expansion",
"air condit$": "air conditioner",
"double pole type chf breaker": "double pole type ch breaker",
"mast 5 er": "master",
"toilet rak": "toilet rack",
"govenore": "governor",
"in wide": "in white",
"shepard hook": "shepherd hook",
"frost fee": "frost free",
"kitchen aide": "kitchen aid",
"saww horse": "saw horse",
"weather striping": "weatherstripper",
"'girls": "girl",
"girl's": "girl",
"girls'": "girl",
"girls": "girl",
"girlz": "girl",
"boy's": "boy",
"boys'": "boy",
"boys": "boy",
"men's": "man",
"mens'": "man",
"mens": "mam",
"men": "man",
"women's": "woman",
"womens'": "woman",
"womens": "woman",
"women": "woman",
"kid's": "kid",
"kids'": "kid",
"kids": "kid",
"children's": "kid",
"childrens'": "kid",
"childrens": "kid",
"children": "kid",
"child": "kid",
"bras": "bra",
"bicycles": "bike",
"bicycle": "bike",
"bikes": "bike",
"refridgerators": "fridge",
"refrigerator": "fridge",
"refrigirator": "fridge",
"freezer": "fridge",
"memories": "memory",
"fragance": "perfume",
"fragrance": "perfume",
"cologne": "perfume",
"anime": "animal",
"assassinss": "assassin",
"assassin's": "assassin",
"assassins": "assassin",
"bedspreads": "bedspread",
"shoppe": "shop",
"extenal": "external",
"knives": "knife",
"kitty's": "kitty",
"levi's": "levi",
"squared": "square",
"rachel": "rachael",
"rechargable": "rechargeable",
"batteries": "battery",
"seiko's": "seiko",
"ounce": "oz"
}
#### end of anoter_replacent_dict


valuable_words_list=['tv','downrod', 'sillcock', 'shelving', 'luminaire', 'paracord', 'ducting', \
    'recyclamat', 'rebar', 'spackling', 'hoodie', 'placemat', 'innoculant', 'protectant', \
    'colorant', 'penetrant', 'attractant', 'bibb', 'nosing', 'subflooring', 'torchiere', 'thhn',\
    'lantern','epoxy','cloth','trim','adhesive','light','lights','saw','pad','polish','nose','stove',\
    'elbow','elbows','lamp','door','doors','pipe','bulb','wood','woods','wire','sink','hose','tile','bath','table','duct',\
    'windows','mesh','rug','rugs','shower','showers','wheels','fan','lock','rod','mirror','cabinet','shelves','paint',\
    'plier','pliers','set','screw','lever','bathtub','vacuum','nut', 'nipple','straw','saddle','pouch','underlayment',\
    'shade','top', 'bulb', 'bulbs', 'paint', 'oven', 'ranges', 'sharpie', 'shed', 'faucet',\
    'finish','microwave', 'can', 'nozzle', 'grabber', 'tub', 'angles','showerhead', 'dehumidifier', \
    'shelving', 'urinal', 'mdf']

not_so_valuable_words_list= ['aaa','off','impact','square','shelves','finish','ring','flood','dual','ball','cutter',\
'max','off','mat','allure','diamond','drive', 'edge','anchor','walls','universal','cat', 'dawn','ion','daylight',\
'roman', 'weed eater', 'restore', 'design', 'caddy', 'pole caddy', 'jet', 'classic', 'element', 'aqua',\
'terra', 'decora', 'ez', 'briggs', 'wedge', 'sunbrella',  'adorne', 'santa', 'bella', 'duck', 'hotpoint',\
'duck', 'tech', 'titan', 'powerwasher', 'cooper lighting', 'heritage', 'imperial', 'monster', 'peak',
'bell', 'drive', 'trademark', 'toto', 'champion', 'shop vac', 'lava', 'jet', 'flood', \
'roman', 'duck', 'magic', 'allen', 'bunn', 'element', 'international', 'larson', 'tiki', 'titan', \
 'space saver', 'cutter', 'scotch', 'adorne', 'ball', 'sunbeam', 'fatmax', 'poulan', 'ring', 'sparkle', 'bissell', \
 'universal', 'paw', 'wedge', 'restore', 'daylight', 'edge', 'americana', 'wacker', 'cat', 'allure', 'bonnie plants', \
 'troy', 'impact', 'buffalo', 'adams', 'jasco', 'rapid dry', 'aaa', 'pole caddy', 'pac', 'seymour', 'mobil', \
 'mastercool', 'coca cola', 'timberline', 'classic', 'caddy', 'sentry', 'terrain', 'nautilus', 'precision', \
 'artisan', 'mural', 'game', 'royal', 'use', 'dawn', 'task', 'american line', 'sawtrax', 'solo', 'elements', \
 'summit', 'anchor', 'off', 'spruce', 'medina', 'shoulder dolly', 'brentwood', 'alex', 'wilkins', 'natural magic', \
 'kodiak', 'metro', 'shelter', 'centipede', 'imperial', 'cooper lighting', 'exide', 'bella', 'ez', 'decora', \
 'terra', 'design', 'diamond', 'mat', 'finish', 'tilex', 'rhino', 'crock pot', 'legend', 'leatherman', 'remove', \
 'architect series', 'greased lightning', 'castle', 'spirit', 'corian', 'peak', 'monster', 'heritage', 'powerwasher',\
 'reese', 'tech', 'santa', 'briggs', 'aqua', 'weed eater', 'ion', 'walls', 'max', 'dual', 'shelves', 'square',\
 'hickory', "vikrell", "e3", "pro series", "keeper", "coastal shower doors", 'cadet','church','gerber','glidden',\
 'cooper wiring devices', 'border blocks', 'commercial electric', 'pri','exteria','extreme', 'veranda',\
 'gorilla glue','gorilla','shark','wen']

not_so_valuable_words_list+=['free','height', 'width', 'depth', 'model','pcs', 'thick','pack','adhesive','steel','cordless', 'aaa' 'b', 'nm', 'hc', 'insulated','gll', 'nutmeg',\
    'pnl', 'sotc','withe','stainless','chrome','beige','max','acrylic', 'cognac', 'cherry', 'ivory','electric','fluorescent', 'recessed', 'matte',\
    'propane','sku','brushless','quartz','gfci','shut','sds','value','brown','white','black','red','green','yellow','blue','silver','pink',\
    'gray','gold','thw','medium','type','flush',"metaliks", 'metallic', 'amp','btu','gpf','pvc','mil','gcfi','plastic', 'vinyl','aaa',\
    'aluminum','brass','antique', 'brass','copper','nickel','satin','rubber','porcelain','hickory','marble','polyacrylic','golden','fiberglass',\
    'nylon','lmapy','maple','polyurethane','mahogany','enamel', 'enameled', 'linen','redwood', 'sku','oak','quart','abs','travertine', 'resin',\
    'birch','birchwood','zinc','pointe','polycarbonate', 'ash', 'wool', 'rockwool', 'teak','alder','frp','cellulose','abz', 'male', 'female', 'used',\
    'hepa','acc','keyless','aqg','arabesque','polyurethane', 'polyurethanes','ardex','armorguard','asb', 'motion','adorne','fatpack',\
    'fatmax','feet','ffgf','fgryblkg', 'douglas', 'fir', 'fleece','abba', 'nutri', 'thermal','thermoclear', 'heat', 'water', 'systemic',\
    'heatgasget', 'cool', 'fusion', 'awg', 'par', 'parabolic', 'tpi', 'pint', 'draining', 'rain', 'cost', 'costs', 'costa','ecostorage',
    'mtd', 'pass', 'emt', 'jeld', 'npt', 'sch', 'pvc', 'dusk', 'dawn', 'lathe','lows','pressure', 'round', 'series','impact', 'resistant','outdoor',\
    'off', 'sawall', 'elephant', 'ear', 'abb', 'baby', 'feedback', 'fastback','jumbo', 'flexlock', 'instant', 'natol', 'naples','florcant',\
    'canna','hammock', 'jrc', 'honeysuckle', 'honey', 'serrano','sequoia', 'amass', 'ashford', 'gal','gas', 'gasoline', 'compane','occupancy',\
    'home','bakeware', 'lite', 'lithium', 'golith','gxwh',  'wht', 'heirloom', 'marine', 'marietta', 'cambria', 'campane','birmingham',\
    'bellingham','chamois', 'chamomile', 'chaosaw', 'chanpayne', 'thats', 'urethane', 'champion', 'chann', 'mocha', 'bay', 'rough',\
    'undermount', 'price', 'prices', 'way', 'air', 'bazaar', 'broadway', 'driveway', 'sprayway', 'subway', 'flood', 'slate', 'wet',\
    'clean', 'tweed', 'weed', 'cub', 'barb', 'salem', 'sale', 'sales', 'slip', 'slim', 'gang', 'office', 'allure', 'bronze', 'banbury',\
    'tuscan','tuscany', 'refinishing', 'fleam','schedule', 'doeskin','destiny', 'mean', 'hide', 'bobbex', 'pdi', 'dpdt', 'tri', 'order',\
    'kamado','seahawks','weymouth', 'summit','tel','riddex', 'alick','alvin', 'ano', 'assy', 'grade', 'barranco', 'batte','banbury',\
    'mcmaster', 'carr', 'ccl', 'china', 'choc', 'colle', 'cothom', 'cucbi', 'cuv', 'cwg', 'cylander', 'cylinoid', 'dcf', 'number', 'ultra',\
    'diat','discon', 'disconnect', 'plantation', 'dpt', 'duomo', 'dupioni', 'eglimgton', 'egnighter','ert','euroloft', 'everready',\
    'felxfx', 'financing', 'fitt', 'fosle', 'footage', 'gpf','fro', 'genis', 'giga', 'glu', 'gpxtpnrf', 'size', 'hacr', 'hardw',\
    'hexagon', 'hire', 'hoo','number','cosm', 'kelston', 'kind', 'all', 'semi', 'gloss', 'lmi', 'luana', 'gdak', 'natol', 'oatu',\
    'oval', 'olinol', 'pdi','penticlea', 'portalino', 'racc', 'rads', 'renat', 'roc', 'lon', 'sendero', 'adora', 'sleave', 'swu',
    'tilde', 'cordoba', 'tuvpl','yel', 'acacia','mig','parties','alkaline','plexiglass', 'iii', 'watt']



df_all = pd.concat((df_train, df_test), axis=0, ignore_index=True)

df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')

df_all['search_term_replaced'] = df_all['search_term'].map(lambda x:spell_correction(x))
#print(df_all[['search_term','search_term_replaced']][2705:2707])

#df_all['search_term_replaced'] = df_all['search_term_replaced'].map(lambda x: " ".join(\
#        [another_replacement_dict[w] if w in another_replacement_dict.keys() else w \
         #for w in x.split()]))
#print(df_all[['search_term','search_term_replaced']][1923:1925])


#print(df_all['search_term'][200:203].map(lambda x: max([int(w in valuable_words_list) for w in x.split()]) ))

#print(df_all['search_term'][1216:1219].map(lambda x: max([int(w in not_so_valuable_words_list) for w in x.split()]) ))

df_all['search_term'] = df_all['search_term_replaced']


df_all['search_term'] = df_all['search_term'].map(lambda x: str_stemmer(x))
df_all['product_title'] = df_all['product_title'].map(lambda x: str_stemmer(x))
df_all['product_description'] = df_all['product_description'].map(lambda x: str_stemmer(x))

df_all['len_of_query'] = df_all['search_term'].map(lambda x: len(x.split())).astype(np.int64)

df_all['product_info'] = df_all['search_term'] + '\t' + df_all['product_title'] + '\t' + df_all['product_description']

df_all['word_in_title'] = df_all['product_info'].map(lambda x: str_common_word(x.split('\t')[0], x.split('\t')[1]))

df_all['word_in_description'] = df_all['product_info'].map(lambda x: str_common_word(x.split('\t')[0], x.split('\t')[2]))

df_all = df_all.drop(['search_term', 'product_title', 'product_description', 'product_info'], axis=1)

df_train = df_all.iloc[:num_train]
df_test = df_all[num_train:]
id_test = df_test['id']

y_train = df_train['relevance'].values
X_train = df_train.drop(['id', 'relevance'], axis=1).values
X_test = df_test.drop(['id', 'relevance'], axis=1).values

rf = RandomForestRegressor(n_estimators=15, max_depth=6, random_state=0)
clf = BaggingRegressor(rf, n_estimators=45, max_samples=0.1, random_state=25)
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)

pd.DataFrame({'id': id_test, 'relevance': y_predict}).to_csv('submission2_rf_bagging.csv', index=False)

stop_w = ['for', 'xbi', 'and', 'in', 'th','on','sku','with','what','from','that','less','er','ing'] #'electr','paint','pipe','light','kitchen','wood','outdoor','door','bathroom'
strNum = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}

def str_stem(s):
    if isinstance(s, str):
        s = re.sub(r"(\w)\.([A-Z])", r"\1 \2", s) #Split words with a.A
        #s = re.sub(r'( [a-z]+)([A-Z][a-z])', r'\1 \2', s)
        s = s.lower()
        s = s.replace("  "," ")
        s = re.sub(r"([0-9]),([0-9])", r"\1\2", s)
        s = s.replace(","," ")
        s = s.replace("$"," ")
        s = s.replace("?"," ")
        s = s.replace("-"," ")
        s = s.replace("//","/")
        s = s.replace("..",".")
        s = s.replace(" / "," ")
        s = s.replace(" \\ "," ")
        s = s.replace("."," . ")
        s = re.sub(r"(^\.|/)", r"", s)
        s = re.sub(r"(\.|/)$", r"", s)
        s = re.sub(r"([0-9])([a-z])", r"\1 \2", s)
        s = re.sub(r"([a-z])([0-9])", r"\1 \2", s)
        s = s.replace(" x "," xbi ")
        s = re.sub(r"([a-z])( *)\.( *)([a-z])", r"\1 \4", s)
        s = re.sub(r"([a-z])( *)/( *)([a-z])", r"\1 \4", s)
        s = s.replace("*"," xbi ")
        s = s.replace(" by "," xbi ")
        s = re.sub(r"([0-9])( *)\.( *)([0-9])", r"\1.\4", s)
        s = re.sub(r"([0-9]+)( *)(inches|inch|in|')\.?", r"\1in. ", s)
        s = re.sub(r"([0-9]+)( *)(foot|feet|ft|'')\.?", r"\1ft. ", s)
        s = re.sub(r"([0-9]+)( *)(pounds|pound|lbs|lb)\.?", r"\1lb. ", s)
        s = re.sub(r"([0-9]+)( *)(square|sq) ?\.?(feet|foot|ft)\.?", r"\1sq.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(cubic|cu) ?\.?(feet|foot|ft)\.?", r"\1cu.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1gal. ", s)
        s = re.sub(r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1oz. ", s)
        s = re.sub(r"([0-9]+)( *)(centimeters|cm)\.?", r"\1cm. ", s)
        s = re.sub(r"([0-9]+)( *)(milimeters|mm)\.?", r"\1mm. ", s)
        s = s.replace("°"," degrees ")
        s = re.sub(r"([0-9]+)( *)(degrees|degree)\.?", r"\1deg. ", s)
        s = s.replace(" v "," volts ")
        s = re.sub(r"([0-9]+)( *)(volts|volt)\.?", r"\1volt. ", s)
        s = re.sub(r"([0-9]+)( *)(watts|watt)\.?", r"\1watt. ", s)
        s = re.sub(r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1amp. ", s)
        s = s.replace("  "," ")
        s = s.replace(" . "," ")
        #s = (" ").join([z for z in s.split(" ") if z not in stop_w])
        s = (" ").join([str(strNum[z]) if z in strNum else z for z in s.split(" ")])
        s = (" ").join([stemmer.stem(z) for z in s.split(" ")])

        s = s.lower()
        s = s.replace("toliet","toilet")
        s = s.replace("airconditioner","air condition")
        s = s.replace("vinal","vinyl")
        s = s.replace("vynal","vinyl")
        s = s.replace("skill","skil")
        s = s.replace("snowbl","snow bl")
        s = s.replace("plexigla","plexi gla")
        s = s.replace("rustoleum","rust oleum")
        s = s.replace("whirpool","whirlpool")
        s = s.replace("whirlpoolga", "whirlpool ga")
        s = s.replace("whirlpoolstainless","whirlpool stainless")
        return s
    else:
        return "null"

def seg_words(str1, str2):
    str2 = str2.lower()
    str2 = re.sub("[^a-z0-9./]"," ", str2)
    str2 = [z for z in set(str2.split()) if len(z)>2]
    words = str1.lower().split(" ")
    s = []
    for word in words:
        if len(word)>3:
            s1 = []
            s1 += segmentit(word,str2,True)
            if len(s)>1:
                s += [z for z in s1 if z not in ['er','ing','s','less'] and len(z)>1]
            else:
                s.append(word)
        else:
            s.append(word)
    return (" ".join(s))

def segmentit(s, txt_arr, t):
    st = s
    r = []
    for j in range(len(s)):
        for word in txt_arr:
            if word == s[:-j]:
                r.append(s[:-j])
                #print(s[:-j],s[len(s)-j:])
                s=s[len(s)-j:]
                r += segmentit(s, txt_arr, False)
    if t:
        i = len(("").join(r))
        if not i==len(st):
            r.append(st[i:])
    return r

def str_common_word(str1, str2):
    words, cnt = str1.split(), 0
    for word in words:
        if str2.find(word)>=0:
            cnt+=1
        # new for edit distance
        if cnt == 0 and len(word)>3:
            s1 = [z for z in list(set(str2.split(" "))) if abs(len(z)-len(word))<2]
            t1 = sum([1 for z in s1 if edit_distance(z, word)<2])
            if t1 > 1:
                cnt+=0.5
    return cnt

def str_whole_word(str1, str2, i_):
    cnt = 0
    while i_ < len(str2):
        i_ = str2.find(str1, i_)
        if i_ == -1:
            return cnt
        else:
            cnt += 1
            i_ += len(str1)
    return cnt

def fmean_squared_error(ground_truth, predictions):
    fmean_squared_error_ = mean_squared_error(ground_truth, predictions)**0.5
    return fmean_squared_error_

RMSE  = make_scorer(fmean_squared_error, greater_is_better=False)

class cust_regression_vals(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self
    def transform(self, hd_searches):
        d_col_drops=['id','relevance','search_term','product_title','product_description','product_info','attr','brand']
        hd_searches = hd_searches.drop(d_col_drops,axis=1).values
        return hd_searches

class cust_txt_col(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, x, y=None):
        return self
    def transform(self, data_dict):
        return data_dict[self.key].apply(str)

df_all['search_term'] = df_all['search_term'].map(lambda x:str_stem(x))
df_all['product_title'] = df_all['product_title'].map(lambda x:str_stem(x))
#df_all['product_description'] = df_all['product_description'].map(lambda x:str_stem(x))
df_all['brand'] = df_all['brand'].map(lambda x: str_stem(x))
print("--- Stemming: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['product_info'] = df_all['search_term']+"\t"+df_all['product_title'] +"\t"+df_all['product_description']
print("--- Prod Info: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['len_of_query'] = df_all['search_term'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_title'] = df_all['product_title'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_description'] = df_all['product_description'].map(lambda x:len(x.split())).astype(np.int64)
df_all['len_of_brand'] = df_all['brand'].map(lambda x:len(x.split())).astype(np.int64)
print("--- Len of: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['search_term'] = df_all['product_info'].map(lambda x:seg_words(x.split('\t')[0],x.split('\t')[1]))
print("--- Search Term Segment: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['query_in_title'] = df_all['product_info'].map(lambda x:str_whole_word(x.split('\t')[0],x.split('\t')[1],0))
df_all['query_in_description'] = df_all['product_info'].map(lambda x:str_whole_word(x.split('\t')[0],x.split('\t')[2],0))
print("--- Query In: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['query_last_word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0].split(" ")[-1],x.split('\t')[1]))
df_all['query_last_word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0].split(" ")[-1],x.split('\t')[2]))
print("--- Query Last Word In: %s minutes ---" % round(((time.time() - start_time)/60),2))
df_all['word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
df_all['word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[2]))
df_all['ratio_title'] = df_all['word_in_title']/df_all['len_of_query']
df_all['ratio_description'] = df_all['word_in_description']/df_all['len_of_query']
df_all['attr'] = df_all['search_term']+"\t"+df_all['brand']
df_all['word_in_brand'] = df_all['attr'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
df_all['ratio_brand'] = df_all['word_in_brand']/df_all['len_of_brand']
df_brand = pd.unique(df_all.brand.ravel())
d={}
i = 1000
for s in df_brand:
    d[s]=i
    i+=3
df_all['brand_feature'] = df_all['brand'].map(lambda x:d[x])
df_all['search_term_feature'] = df_all['search_term'].map(lambda x:len(x))

df_train = df_all.iloc[:num_train]
df_test = df_all.iloc[num_train:]

y_train = df_train['relevance']
id_test = df_test['id']

d_col_drops=['id','relevance','search_term','product_title','product_description','product_info','attr','brand']
train2 = df_train[d_col_drops]
test2 = df_test[d_col_drops]
train = df_train.drop(d_col_drops,axis=1)[:]
test =  df_test.drop(d_col_drops,axis=1)[:]

print("--- Features Set: %s minutes ---" % round(((time.time() - start_time)/60),2))

for (train_name, train_series), (test_name, test_series) in zip(train.iteritems(),test.iteritems()):
    if train_series.dtype == 'O':
        train[train_name], tmp_indexer = pd.factorize(train[train_name])
        test[test_name] = tmp_indexer.get_indexer(test[test_name])
    else:
        tmp_len = len(train[train_series.isnull()])
        if tmp_len>0:
            train.loc[train_series.isnull(), train_name] = train_series.mean()
        tmp_len = len(test[test_series.isnull()])
        if tmp_len>0:
            test.loc[test_series.isnull(), test_name] = train_series.mean()

train=pd.concat([train,train2], axis=1)[:]
test=pd.concat([test,test2], axis=1)[:]

xgb_model = xgb.XGBRegressor(learning_rate=0.25, silent=False, objective="reg:linear", nthread=-1, gamma=0, min_child_weight=1, max_delta_step=0,
                 subsample=1, colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1, scale_pos_weight=1,
                 base_score=0.5, seed=0, missing=None)
tfidf = TfidfVectorizer(ngram_range=(1, 1), stop_words='english')
tsvd = TruncatedSVD(n_components=10, random_state = 2016)

clf = pipeline.Pipeline([
        ('union', FeatureUnion(
                    transformer_list = [
                        ('cst',  cust_regression_vals()),
                        ('txt1', pipeline.Pipeline([('s1', cust_txt_col(key='search_term')), ('tfidf1', tfidf), ('tsvd1', tsvd)])),
                        ('txt2', pipeline.Pipeline([('s2', cust_txt_col(key='product_title')), ('tfidf2', tfidf), ('tsvd2', tsvd)])),
                        ('txt3', pipeline.Pipeline([('s3', cust_txt_col(key='product_description')), ('tfidf3', tfidf), ('tsvd3', tsvd)])),
                        ('txt4', pipeline.Pipeline([('s4', cust_txt_col(key='brand')), ('tfidf4', tfidf), ('tsvd4', tsvd)]))
                        ],
                    transformer_weights = {
                        'cst': 1.0,
                        'txt1': 0.5,
                        'txt2': 0.25,
                        'txt3': 0.0,
                        'txt4': 0.5
                        },
                #n_jobs = -1
                )),
        ('xgb_model', xgb_model)])
param_grid = {'xgb_model__max_depth': [5], 'xgb_model__n_estimators': [10]}
model = model_selection.GridSearchCV(estimator = clf, param_grid = param_grid, n_jobs = -1, cv = 2, verbose = 20, scoring=RMSE)
model.fit(train, y_train.values)

print("Best parameters found by grid search:")
print(model.best_params_)
print("Best CV score:")
print(model.best_score_)
print(model.best_score_ + 0.47003199274)

y_pred = model.predict(test)

#print(len(y_pred))
#pd.DataFrame({"id": id_test, "relevance": y_pred}).to_csv('submission_before.csv',index=False)
min_y_pred = min(y_pred)
max_y_pred = max(y_pred)
min_y_train = min(y_train.values)
max_y_train = max(y_train.values)
print(min_y_pred, max_y_pred, min_y_train, max_y_train)
for i in range(len(y_pred)):
    if y_pred[i]<1.0:
        y_pred[i] = 1.0
    if y_pred[i]>3.0:
        y_pred[i] = 3.0
    #y_pred[i] = min_y_train + (((y_pred[i] - min_y_pred)/(max_y_pred - min_y_pred))*(max_y_train - min_y_train))
pd.DataFrame({"id": id_test, "relevance": y_pred}).to_csv('submission_after.csv',index=False)
print("--- Training & Testing: %s minutes ---" % round(((time.time() - start_time)/60),2))
