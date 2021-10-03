import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from collections import Counter

def pattern_check(win_country,freq_list):
    list = []
    for w in freq_list:
        word = w.split("_")
        list = list + word
    word_dict = dict(Counter(list))
    if 'Team1' in word_dict.keys():
        if word_dict['Team1'] >= 2:
            replace_dict1 = {'Team1_Away':win_country+'->Foreign Country','Team1_Home':win_country+'->Motherland','Team1_First Inning':win_country+'->First Inning'}
            replace_dict2 = {'Team2_Away':'Opposite Team->Foreign Country','Team2_Home':'Opposing Team->Motherland','Team2_Second Inning':'Opposing Team->Second Inning'}
            if 'Team1_Away' in freq_list:
                freq_list = [i.replace('Team1_Away', replace_dict1['Team1_Away']) for i in freq_list]
            if 'Team1_Home' in freq_list:
                freq_list = [i.replace('Team1_Home', replace_dict1['Team1_Home']) for i in freq_list]
            if (x in freq_list for x in ['Team2_Away', 'Team2_Home']):
                if 'Team2_Home' in freq_list:
                    freq_list = [i.replace('Team2_Home', replace_dict2['Team2_Home']) for i in freq_list]
                else:
                    freq_list = [i.replace('Team2_Away', replace_dict2['Team2_Away']) for i in freq_list]
            if 'Team2_Second Inning' in freq_list:
                freq_list = [i.replace('Team2_Second Inning', replace_dict2['Team2_Second Inning']) for i in freq_list]
            freq_list = [i.replace('Team1_First Inning', replace_dict1['Team1_First Inning']) for i in freq_list]
            return freq_list

        elif word_dict['Team2'] >= 2:
            replace_dict1 = {'Team2_Away':win_country+'->Foreign Country','Team2_Home':win_country+'->Motherland','Team2_Second Inning':win_country+'->Second Inning'}
            replace_dict2 = {'Team1_Away':'Opposite Team->Foreign Country','Team1_Home':'Opposing Team->Motherland','Team1_First Inning':'Opposing Team->First Inning'}
            if 'Team2_Away' in freq_list:
                freq_list = [i.replace('Team2_Away', replace_dict1['Team2_Away']) for i in freq_list]
            if 'Team2_Home' in freq_list:
                freq_list = [i.replace('Team2_Home', replace_dict1['Team2_Home']) for i in freq_list]
            if (x in freq_list for x in ['Team1_Away', 'Team1_Home']):
                if 'Team1_Home' in freq_list:
                    freq_list = [i.replace('Team1_Home', replace_dict2['Team1_Home']) for i in freq_list]
                else:
                    freq_list = [i.replace('Team1_Away', replace_dict2['Team1_Away']) for i in freq_list]
            if 'Team1_First Inning' in freq_list:
                freq_list = [i.replace('Team1_First Inning', replace_dict2['Team1_First Inning']) for i in freq_list]
            freq_list = [i.replace('Team2_Second Inning', replace_dict1['Team2_Second Inning']) for i in freq_list]
            return freq_list

def arm_rule(team):
    
    data=pd.read_csv('ODI(ARM).csv')
    
    for country in data['Team1'].unique():
        data['Team1'] = data['Team1'].replace(country, 'Team1_'+country)
    
    for country in data['Team2'].unique():
        data['Team2'] = data['Team2'].replace(country, 'Team2_'+country)
    
    for item in data['Venue_Team1'].unique():
        data['Venue_Team1'] = data['Venue_Team1'].replace(item, 'Team1_'+item)
    
    for item in data['Venue_Team2'].unique():
        data['Venue_Team2'] = data['Venue_Team2'].replace(item, 'Team2_'+item)
    
    for item in data['Inning_Team1'].unique():
        data['Inning_Team1'] = data['Inning_Team1'].replace(item, 'Team1_'+item+' Inning')
    
    for item in data['Inning_Team2'].unique():
        data['Inning_Team2'] = data['Inning_Team2'].replace(item, 'Team2_'+item+' Inning')
    
    for country in data['Winner'].unique():
        data['Winner'] = data['Winner'].replace(country, country+'_Winner')
    
    df_new = data
    
    Team1ColumnDummy = pd.get_dummies(df_new['Team1'])
    Team2ColumnDummy = pd.get_dummies(df_new['Team2'])
    VenueTeam1ColumnDummy = pd.get_dummies(df_new['Venue_Team1'])
    VenueTeam2ColumnDummy = pd.get_dummies(df_new['Venue_Team2'])
    InningTeam1ColumnDummy = pd.get_dummies(df_new['Inning_Team1'])
    InningTeam2ColumnDummy = pd.get_dummies(df_new['Inning_Team2'])
    WinnerColumnDummy = pd.get_dummies(df_new['Winner'])
    
    df_new = pd.concat((df_new, Team1ColumnDummy, Team2ColumnDummy,  VenueTeam1ColumnDummy, VenueTeam2ColumnDummy, InningTeam1ColumnDummy, InningTeam2ColumnDummy, WinnerColumnDummy), axis=1)
    
    df_new = df_new.drop(['Team1', 'Team2', 'Inning_Team1', 'Inning_Team2', 'Venue_Team1', 'Venue_Team2', 'Winner'],axis= 1)
    
    frequent_itemsets = apriori(df_new, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    input_val = team
    pass_val = input_val+'_Winner'
    result = rules[rules['antecedents'] == {pass_val}]
    return_list = []
    for i in result['consequents']:
        if len(i) >= 2 and len(i) < 4:
            fp = pattern_check(input_val,list(i))
            if fp == None or 'Team1_'+input_val in fp or 'Team2_'+input_val in fp:
                continue
            #print(fp)
            return_list.append(fp)
    return return_list

