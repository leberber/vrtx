import dash_mantine_components as dmc
from utils.helpers import iconify
import ast

def prepare_metadata(df):
    df['value'] = df['value'].fillna('')
    df['stepID'] = df['stepID'].astype('str')
    df['options'] = df['options'].fillna('[]')
    df['options'] = df['options'].apply(ast.literal_eval)

    records= df.to_dict('records')

    transformed_data = {}
    for item in records:

        step_id = item['stepID']
        if step_id not in transformed_data:
            transformed_data[step_id] = {
                'stepID': item['stepID'],
                'stepName': item['stepName'],
                'stepIcon': item['stepIcon'],
                'stepDescription': item['stepDescription'],
                'questions': []
            }
        
        question_details = {
            'questionID': item['questionID'],
            'question': item['question'],
            'options': item['options'],
            'value': item['value'],
            'input_type': item['input_type'],
            'description': item['description']
        }
        transformed_data[step_id]['questions'].append(question_details)

    return transformed_data


options_style  = {'label':{'color':'gray'}}

def label(label, description='', icon='duo-icons:info' ):
    return dmc.Box(
        display='flex',
        mt = 20,
        children = [
                dmc.Tooltip(
                    dmc.Box(iconify(icon, color = '#80b3ff', width = 25) ),
                    label=description,
                    withArrow=True,
                    multiline = True,
                    position = 'botton-start',
                    fw = 400,
                    w = 300,
            ),
            dmc.Text(label, c = '#404040', m = 0)

        ]
    )


def checkbox(item_dict):
    myInput =  dmc.CheckboxGroup(
        ml = 20,
        id={'type':'forms-user-inputs', 'index':f"{item_dict['stepID']}_{item_dict['questionID']}"},
        value=item_dict['value'],
        children=dmc.Group(
            children = [
                dmc.Checkbox(
                    label=item, 
                    value=item, size="sm", styles =options_style
                ) for item in item_dict['options'] 
            ]
        )
    )
    return dmc.Box(
        children = [
            label(item_dict['question'], description=item_dict['description'], ),
            myInput
        ]
    )

def radio(item_dict):
    myInput =  dmc.RadioGroup(
        ml = 20,
        id={'type':'forms-user-inputs', 'index':f"{item_dict['stepID']}_{item_dict['questionID']}"},
        value=item_dict['value'],
        children=dmc.Group(
            children = [
                dmc.Radio(
                    label = item, 
                    value=item, 
                    styles =options_style
                ) for item in item_dict['options']
            ]
        )
    )
    return dmc.Box(
        children = [
            label(item_dict['question'], description=item_dict['description'] ),
            myInput
        ]
    )

def segmentcontrol(item_dict):
    myInput = dmc.SegmentedControl(
        ml = 20,
        size = 'sm',
        radius = 'md',
        value = item_dict['value'],
        id={'type':'forms-user-inputs', 'index':f"{item_dict['stepID']}_{item_dict['questionID']}"},
        data=item_dict['options'],
    )

    return  dmc.Box(
        children = [
            label(item_dict['question'], description=item_dict['description']),
            myInput
        ]
    )

def chip(item_dict, multiple=False):
    myInput =  dmc.ChipGroup(
        id={'type':'forms-user-inputs', 'index':f"{item_dict['stepID']}_{item_dict['questionID']}"},
        deselectable=multiple,
        value=item_dict['value'],
        multiple = multiple,
        children =[
            dmc.Chip(
                item, 
                value=item,  
                variant='light',
                styles =options_style
            ) for item in item_dict['options']
        ]
    )
    return  dmc.Box(
        children = [
            label(item_dict['question'], description=item_dict['description']),
            dmc.Group(myInput, gap =4, ml = 20)
        ]
    )
 
def textinput(item_dict):
    myInput =  dmc.TextInput( 
        ml = 20,
        id={'type':'forms-user-inputs', 'index':f"{item_dict['stepID']}_{item_dict['questionID']}"},
        placeholder=item_dict['value']
    )
    return  dmc.Box(
        children = [
            label(item_dict['question'], description=item_dict['description']),
            dmc.Group(myInput, gap =4)
        ]
    )

def make_questions (step):
    step_questions = step['questions']
    l = []
    for item_dict in step_questions:
        item_dict['stepID'] = step['stepID']
        if item_dict['input_type'] == 'Radio':
            item = radio(item_dict)
        elif item_dict['input_type'] == 'Checkbox':
            item = checkbox(item_dict)
        elif item_dict['input_type'] == 'CheckboxChip':
            item = chip(item_dict, multiple=True)
        elif item_dict['input_type'] == 'RadioChip':
            item = chip(item_dict, multiple=False)
        elif item_dict['input_type'] == 'SegmentedControl':
            item = segmentcontrol(item_dict)
        elif item_dict['input_type'] == 'TextInput':
            item = textinput(item_dict)
        else:
            raise ValueError(f"The Input for Question {item_dict['questionID']} is not recognized")

        l.append(item)

    half = len(l) // 2

    return dmc.SimpleGrid(
        cols={ 'base': 1, 'md': 2, 'lg': 2, 'xl':2 },
        spacing={"base": 10, "sm": "xl"},
        verticalSpacing={"base": "md", "sm": "xl"},
        children=[
            dmc.Box(l[:half],  p = 10, style = {"boxShadow": "rgba(0, 0, 0, 0.05) 0px 0px 0px 1px", "borderRadius":10}),
            dmc.Box(l[half:], p = 10, style = {"boxShadow": "rgba(0, 0, 0, 0.05) 0px 0px 0px 1px", "borderRadius":15})
        ],
    )
    

def form_progress(data):
    """Calculate the percentage of None values for each group in a dictionary.
    
    Args:
        data (dict): A dictionary where keys are in the format '<group>_<id>' 
                     and values can be any type, including None.
                     
    Returns:
        dict: A dictionary with groups as keys and percentages of None values as values.
    """
    # Initialize dictionaries for total and None counts per group
    total_count = {}
    none_count = {}

    # Count total and None values per group
    for key, value in data.items():
        group = key.split('_')[0]  # Extract group from key
        total_count[group] = total_count.get(group, 0) + 1
        if value is None or value ==[] or value =='':
            none_count[group] = none_count.get(group, 0) + 1

    # Calculate the percentage of None values for each group
    none_percentage = {
        group: (none_count.get(group, 0) / total_count[group]) * 100
        for group in total_count
    }
    
    return none_percentage
