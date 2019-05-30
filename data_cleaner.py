import json

with open('lv_elections/results_2.json') as json_file:
    data = json.load(json_file)
    clean_data = []
    for i in data[1:]:
        #print(i['votes'])
        clean_votes = {k.lower().replace('.','_'): int(v) for k, v in i['votes'].items() if v != '-'}
        clean_values = {k.lower(): str(v).replace(',','').replace('%','') for k, v in i.items() if k != 'votes'}
        clean_values['votes'] = clean_votes
        clean_data.append(clean_values)
    with open('clean_data.json', 'w') as outfile:
        json.dump(clean_data, outfile)