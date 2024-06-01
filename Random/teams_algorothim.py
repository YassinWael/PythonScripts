# An algorthim to generate a given number of matches with based number of teams, no teams can replay each other.
from random import choices
from icecream import ic
from math import ceil
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
teams = ["wael","reham","yassin","mohamed"]




def random_matches(teams,total_matches=10):
    """
    Generate random matches between teams.

    Args:
        teams (list): List of team names.
        total_matches (int): Total number of matches to generate.

    Returns:
        tuple: A tuple containing matches, number of matches generated, and played matches count.
    """
    used_teams = []
    
    
    
    
    matches = []
    
    
    played_matches_count = {team:0 for team in teams}
    ic(played_matches_count) 

    
    max_number = ceil(total_matches/len(teams)) #max number one team is allowed to play
    
    ic(max_number)
    try:
        while len(matches) < total_matches:
            if len(teams) !=2: #only two teams are left.
                weights = [1 + (played_matches_count[i]**30) for i in teams][::-1] # Flipped the list so that the most played team has less chance of being chosen.
                team1 = choices(teams,weights)[0]
                teams.pop(teams.index(team1)) # so that it doesn't get chosen for team 2 
                weights = [1 + played_matches_count[i] for i in teams][::-1] # Flipped the list so that the most played team has less chance of being chosen.
                team2 = choices(teams,weights)[0]
                teams.pop(teams.index(team2))

                teams_match = (team1,team2) #  A tuple to compare if teams have fought before or not.
                if not teams_match in used_teams and played_matches_count[team1] < max_number and played_matches_count[team2] < max_number:
                    matches.append(teams_match)

                    played_matches_count[team1] = played_matches_count[team1]+1
                    played_matches_count[team2] = played_matches_count[team2]+1
                
                    teams.append(team1)
                    teams.append(team2)
                    ic(len(matches))
                    ic(played_matches_count)

                    
                    used_teams.append(teams_match)
                    used_teams.append(teams_match[::-1])
                else:
                    if played_matches_count[team1] < max_number:
                        teams.append(team1)
                    else:
                        ic(f"{team1} has been removed.")
                    if played_matches_count[team2] < max_number:
                        teams.append(team2)
                    else:
                        ic(f"{team2} has been removed.")
            else:
                matches.append((teams[0],teams[1]))
                return matches,len(matches),played_matches_count
                

    except Exception as e:
        ic('-------------------------------------------------------')
        print(f"Exited with error: {e}, {len(matches)} matches in total.")
        print(weights,teams)
        ic('-------------------------------------------------------')
        return matches,len(matches),played_matches_count

        




   
    return matches,len(matches),played_matches_count


a = random_matches(teams)
matches = [list(match) for match in a [0]] #converting to a list of lists for pdf creation.
matches.append(["Matches"])
matches = matches[::-1]

doc = SimpleDocTemplate("matches.pdf",pagesize=A4)

table = Table(data=matches)

style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0,1), (-1, -1), .8, colors.black)])
table.setStyle(style)

doc.build([table])
print("The pdf file for the match has been generated, Please check the working directory.")





# TO-DO: Fix the pdf styling, better tables, readability...etc



