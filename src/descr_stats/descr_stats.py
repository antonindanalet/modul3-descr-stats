import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def descr_stats(df_module_3):
    df_module_3 = remove_partial_answers(df_module_3)
    df_module_3 = remove_respondents_without_mobility_data(df_module_3)
    df_percentage = compute_percentages_and_confidence_intervals(df_module_3)
    visualize_percentage(df_percentage)


def compute_percentages_and_confidence_intervals(df_module_3):
    # Restructure data: from "SR_Sector_Public_transport : 1, 5, 3, etc." to "SR_Sector_Public_transport_1: 1, 0, etc.
    list_of_questions = ['SR_Sector_Public_transport',
                         'SR_Sector_Bike',
                         'SR_Sector_Road',
                         'SR_Sector_Walk',
                         'SR_Sector_Environment',
                         'SR_Measure_Car_Bottlenecks',
                         'SR_Measure_Car_Extension',
                         'SR_Measure_Car_Cities',
                         'SR_Measure_Car_Safety',
                         'SR_Measure_Car_Information',
                         'SR_Measure_Public_transport_Long_distance',
                         'SR_Measure_Public_transport_Local',
                         'SR_Measure_Public_transport_Vehicles',
                         'SR_Measure_Public_transport_Seats',
                         'SR_Measure_Public_transport_Comfort',
                         'SR_Measure_Biking_Paths',
                         'SR_Measure_Biking_Lanes',
                         'SR_Measure_Biking_Parking',
                         'SR_Measure_Biking_Sharing',
                         'SR_Measure_Biking_Zone30',
                         'SR_Measure_Walking_Zone20',
                         'SR_Measure_Walking_Safety',
                         'SR_Measure_Walking_Roadway_design',
                         'SR_Measure_Walking_Public_space',
                         'SR_Measure_Walking_Routes',
                         'SR_Measure_Environment_Electric_car',
                         'SR_Measure_Environment_New_vehicles',
                         'SR_Measure_Environment_Noise',
                         'SR_Measure_Environment_Traffic_ban',
                         'SR_Measure_Environment_Fuel_consumption',
                         'SR_Measure_Innovation_Housing',
                         'SR_Measure_Innovation_Mobility_costs',
                         'SR_Measure_Innovation_Autonomous_vehicles',
                         'SR_Measure_Innovation_Sharing',
                         'SR_Measure_Innovation_Telecommuting']
    for columns_stated_ranking in list_of_questions:
        new_columns = pd.DataFrame({columns_stated_ranking + f"_{i}": df_module_3[columns_stated_ranking] == i
                                    for i in range(1, 6)})
        df_module_3 = pd.concat([df_module_3, new_columns], axis=1)
        # Add the variable for the ranking (answered 1, 2 or (half of) 3)
        name_new_variable_1 = columns_stated_ranking + '_sum_1_2_half_3'
        name_new_variable_2 = columns_stated_ranking + '_sum_4_5_half_3'
        df_module_3[name_new_variable_1] = df_module_3.apply(lambda row: define_ranking_1(row, columns_stated_ranking),
                                                             axis=1)
        df_module_3[name_new_variable_2] = df_module_3.apply(lambda row: define_ranking_2(row, columns_stated_ranking),
                                                             axis=1)

    # Compute weighted average and confidence interval for each group of questions
    df_for_csv = pd.DataFrame(columns=['Variable',
                                       '1', '1 (+/-)',
                                       '2', '2 (+/-)',
                                       '3', '3 (+/-)',
                                       '4', '4 (+/-)',
                                       '5', '5 (+/-)',
                                       'Sample',
                                       '1+2+0.5*3', '1+2+0.5*3 (+/-)'])
    for question in list_of_questions:
        # Create the raw to be added, beginning with the variable's name
        list_of_questions_with_ranking = [question + '_' + str(i) for i in range(1, 6)]
        # Keep only the people who have answered to theses particular questions
        df_module_3_with_answers = df_module_3[df_module_3[list_of_questions_with_ranking[0][:-2]] != -99]
        percentage_and_sample = get_weighted_avg_and_std(df_module_3_with_answers, weights='WP', percentage=True,
                                                         list_of_columns=list_of_questions_with_ranking)
        dict_percentage = percentage_and_sample[0]
        sample = percentage_and_sample[1]
        list_of_values_for_row = [question]
        for i in range(1, 6):
            list_of_values_for_row.append(dict_percentage[question + '_' + str(i)][0])
            list_of_values_for_row.append(dict_percentage[question + '_' + str(i)][1])
        # Add the sample size to the raw
        list_of_values_for_row.append(sample)
        # Add the variable used to rank the measures
        name_ranking_variable_1 = question + '_sum_1_2_half_3'
        name_ranking_variable_2 = question + '_sum_4_5_half_3'
        percentage_and_sample_rank = get_weighted_avg_and_std(df_module_3_with_answers, weights='WP', percentage=True,
                                                              list_of_columns=[name_ranking_variable_1,
                                                                               name_ranking_variable_2])
        percentage_rank = percentage_and_sample_rank[0]
        percentage_rank_sum_1_2_half_3 = percentage_rank[name_ranking_variable_1][0]
        list_of_values_for_row.append(percentage_rank_sum_1_2_half_3)
        confidence_interval_rank_sum_1_2_half_3 = percentage_rank[name_ranking_variable_1][1]
        list_of_values_for_row.append(confidence_interval_rank_sum_1_2_half_3)
        # Add the raw at the end of the df / csv file
        df_for_csv.loc[len(df_for_csv.index)] = list_of_values_for_row
    output_folder = Path("../data/output/table/")
    df_for_csv.to_csv(output_folder / 'module_3_results.csv', index=False, sep=';')
    # Remove unnecessary variables for the next steps
    df_for_csv.drop(columns=['1+2+0.5*3', '1+2+0.5*3 (+/-)',
                             'Sample',
                             '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'], inplace=True)
    return df_for_csv


def define_ranking_1(row, columns_stated_ranking):
    if row[columns_stated_ranking] == 1:
        return 1
    elif row[columns_stated_ranking] == 2:
        return 1
    elif row[columns_stated_ranking] == 3:
        return 0.5
    else:
        return 0


def define_ranking_2(row, columns_stated_ranking):
    if row[columns_stated_ranking] == 4:
        return 1
    elif row[columns_stated_ranking] == 5:
        return 1
    elif row[columns_stated_ranking] == 3:
        return 0.5
    else:
        return 0


def remove_respondents_without_mobility_data(df_module_3):
    df_module_3 = df_module_3[df_module_3['with_mobility_data'] == True]
    return df_module_3


def visualize_percentage(df_percentage):
    """ This functions generates two types of graphical representations of the ranking questions. """
    ''' Visualize as bar plot '''
    output_folder = Path("../data/output/bar_plot/")
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_percentage['sum_1_2'] = df_percentage['1'] + df_percentage['2']
    visualize_percentage_general(df_percentage, output_folder)
    visualize_percentage_car(df_percentage, output_folder)
    visualize_percentage_public_transport(df_percentage, output_folder)
    visualize_percentage_biking(df_percentage, output_folder)
    visualize_percentage_walking(df_percentage, output_folder)
    visualize_percentage_environment(df_percentage, output_folder)
    visualize_percentage_innovation(df_percentage, output_folder)
    ''' Visualize as divergent bar plot '''
    output_folder = Path("../data/output/divergent_bar_plot/")
    # General
    title = 'Secteurs dans lesquels des am??liorations sont les plus importantes'
    dict_measures = {'SR_Sector_Public_transport': 'Am??lioration des transports publics (train, bus, tram)',
                     'SR_Sector_Bike': 'Am??lioration des am??nagements cyclables (y compris v??lo ??lectrique)',
                     'SR_Sector_Road': 'Am??lioration du trafic routier (voiture, moto)',
                     'SR_Sector_Walk': 'Am??lioration des am??nagements pi??tons',
                     'SR_Sector_Environment': 'R??duction de l???impact environnemental du trafic'}
    output_name = 'Stated_Ranking_General.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Car
    title = 'Mesures li??es au transport individuel motoris?? dans lesquels des am??liorations sont les plus importantes'
    dict_measures = {'SR_Measure_Car_Bottlenecks': '??limination des goulets d?????tranglement sur le r??seau existant\n'
                                                   '(p. ex.??construction d???une voie suppl??mentaire sur une '
                                                   'autoroute)',
                     'SR_Measure_Car_Extension': 'Extension du r??seau des routes nationales\n'
                                                 '(p. ex. construction de nouveaux tron??ons autoroutiers)',
                     'SR_Measure_Car_Cities': 'Fluidification du trafic dans les villes et les agglom??rations\n'
                                              '(p. ex. construction de nouveaux contournements,\n'
                                              'remplacement des feux par des giratoires)',
                     'SR_Measure_Car_Safety': 'Renforcement de la s??curit?? routi??re\n'
                                              '(p. ex. travaux d???am??nagement, syst??mes d???aide ?? la conduite)',
                     'SR_Measure_Car_Information': 'Diffusion d???informations sur l?????tat du trafic afin d?????viter les '
                                                   'embouteillages\n'
                                                   '(p. ex. via des applications pour smartphones)'}
    output_name = 'Stated_Ranking_Car.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Public transport
    title = 'Mesures li??es aux transports publics dans lesquels des am??liorations sont les plus importantes'
    dict_measures = {'SR_Measure_Public_transport_Long_distance': 'Am??lioration du trafic longues distances '
                                                                  '(trains)??:\n'
                                                                  'augmentation de la fr??quence ou de la vitesse',
                     'SR_Measure_Public_transport_Local': 'Am??lioration du trafic local et r??gional (RER, tram, '
                                                          'bus)??:\n'
                                                          'augmentation de la fr??quence ou de la vitesse',
                     'SR_Measure_Public_transport_Vehicles': 'Modernisation des trains, des bus et des trams\n'
                                                             '(p. ex. nouveaux v??hicules, acc??s Internet)',
                     'SR_Measure_Public_transport_Seats': 'Plus de places sur les lignes existantes',
                     'SR_Measure_Public_transport_Comfort': 'Am??lioration du confort et de l???efficacit?? lors des '
                                                            'changements\n'
                                                            '(p. ex. signal??tique, raccourcissement des distances,\n'
                                                            'plus de commerces)'}
    output_name = 'Stated_Ranking_PT.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Biking
    title = 'Mesures li??es aux am??nagements cyclables dans lesquels des am??liorations sont les plus importantes'
    dict_measures = {'SR_Measure_Biking_Paths': 'D??veloppement des pistes cyclables',
                     'SR_Measure_Biking_Lanes': 'D??veloppement des bandes cyclables avec marquage color??',
                     'SR_Measure_Biking_Parking': 'D??veloppement des places de stationnement pour v??los',
                     'SR_Measure_Biking_Sharing': 'D??veloppement des syst??mes de v??los en libre-service',
                     'SR_Measure_Biking_Zone30': 'D??veloppement des zones limit??es ?? 30??km/h'}
    output_name = 'Stated_Ranking_Biking.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Walking
    title = 'Mesures li??es aux am??nagements pi??tons dans lesquels des am??liorations sont les plus importantes'
    dict_measures = {'SR_Measure_Walking_Zone20': 'D??veloppement des zones de rencontre limit??es ?? 20??km/h',
                     'SR_Measure_Walking_Safety': 'Renforcement de la s??curit??\n'
                                                  '(??clairage public, am??lioration de la visibilit??)',
                     'SR_Measure_Walking_Roadway_design': 'R??am??nagement de la voirie\n'
                                                          '(p. ex. ??largissement des trottoirs, zones pi??tonnes)',
                     'SR_Measure_Walking_Public_space': 'Renforcement de la convivialit?? de l???espace public\n'
                                                        '(p. ex. plus de bancs, terrasses de caf??s, espaces verts)',
                     'SR_Measure_Walking_Routes': 'Itin??raires plus directs\n'
                                                  '(p. ex. passerelles pour pi??tons, plus de passages pi??tons)'}
    output_name = 'Stated_Ranking_Walking.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Environment
    title = "Mesures li??es ?? l'environnement et l'??nergie dans lesquels des am??liorations sont les plus importantes"
    dict_measures = {'SR_Measure_Environment_Electric_car': 'Mesures de soutien pour les v??hicules ??lectriques\n'
                                                            '(p. ex. plus de bornes de recharge, stationnements r??serv??s)',
                     'SR_Measure_Environment_New_vehicles': 'Incitations financi??res ?? l???achat de nouveaux v??hicules\n'
                                                            '??conomes en ??nergie et ?? faibles ??missions',
                     'SR_Measure_Environment_Noise': 'R??duction du bruit du trafic\n'
                                                     '(p. ex. rev??tements anti-bruit, parois anti-bruit)',
                     'SR_Measure_Environment_Traffic_ban': 'Interdiction de circuler en ville pour les voitures\n'
                                                           'd??passant les valeurs limites d?????missions',
                     'SR_Measure_Environment_Fuel_consumption': 'Prescriptions techniques??:'
                                                                'limitation de la consommation de carburant'}
    output_name = 'Stated_Ranking_Environment.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Innovation
    title = "Mesures innovantes dans lesquels des am??liorations sont les plus importantes"
    dict_measures = {'SR_Measure_Innovation_Housing': 'Davantage de logements et d???emplois dans les villes et les '
                                                      'agglom??rations\n'
                                                      '(d???o?? une r??duction des distances ?? parcourir)',
                     'SR_Measure_Innovation_Mobility_costs': 'Hausse g??n??rale du co??t de la mobilit?? '
                                                             '(voiture et transports publics)',
                     'SR_Measure_Innovation_Autonomous_vehicles': 'Mesures de soutien pour les v??hicules autonomes\n'
                                                                  '(p. ex. modification de lois, exp??riences pilotes)',
                     'SR_Measure_Innovation_Sharing': 'Mesures de soutien pour la mobilit?? partag??e??: '
                                                      'autopartage de type\n'
                                                      'Mobility, covoiturage, syst??mes de pr??t de v??los\n'
                                                      '(p. ex. modification de lois, exp??riences pilotes)',
                     'SR_Measure_Innovation_Telecommuting': 'Soutien aux mod??les de travail flexibles, qui permettent '
                                                            'de r??duire ou\n'
                                                            'de d??caler les d??placements (p. ex. t??l??travail depuis '
                                                            'chez soi ou\n'
                                                            'un autre lieu, libre choix des horaires de travail)'}
    output_name = 'Stated_Ranking_Innovation.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)


def visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,):
    """ Visualize the first ranking questions """
    # Filter the count results of the given question
    list_of_variable_names_of_measures = []
    for key in dict_measures:
        list_of_variable_names_of_measures.append(key)
    df_percentage_1 = df_percentage.loc[df_percentage['Variable'].isin(list_of_variable_names_of_measures)].copy()
    # Change the order of the columns to have priority 1 on the right
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    ''' Define the ranking of measures '''
    # Inspiration for the code:
    # https://stackoverflow.com/questions/23142358/create-a-diverging-stacked-bar-chart-in-matplotlib
    # https://blog.orikami.nl/behind-the-screens-likert-scale-visualization-368557ad72d1
    # Define the middle point of the measures by summing prio 4 & 5 plus half of prio 3
    middles = df_percentage_1[['5', '4']].sum(axis=1) + df_percentage_1['3'] * .5
    longest = middles.max()
    # Insert an invisible column in the dataframe
    invisible_column = (middles - longest).abs()
    df_percentage_1.insert(0, '', invisible_column)
    # Change the order of the rankings, based on the middle point
    df_percentage_1.sort_values(by=[''], inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index=dict_measures,
                                             columns={1: '$\mathregular{1^{re}}$ priorit??',
                                                      2: '$\mathregular{2^e}$ priorit??',
                                                      3: '$\mathregular{3^e}$ priorit??',
                                                      4: '$\mathregular{4^e}$ priorit??',
                                                      5: '$\mathregular{5^e}$ priorit??',
                                                      '': ''})
    # Plot the answers
    sns.set_style("whitegrid", {'axes.grid': False})
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    # Define the color scheme of the Federal Statistical Office (FSO),
    # with white as the first color, for the invisible column
    FSO_colors = [[1, 1, 1],  # white
                  [232 / 255, 89 / 255, 29 / 255],  # dark red
                  [245 / 255, 164 / 255, 40 / 255],  # light red
                  [207 / 255, 208 / 255, 208 / 255],  # grey
                  [177 / 255, 222 / 255, 241 / 255],  # light blue
                  [24 / 255, 154 / 255, 196 / 255]]  # dark blue
    # Plotting the bars with the colors
    ax = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    # Make the "invisible column" transparent, so that we see the grid behind
    for bar in ax.patches[1:5]:
        bar.set_alpha(0.0)
    fig = ax.get_figure()
    plt.title(title)
    # plt.suptitle('Secteurs dans lesquels des am??liorations sont les plus importantes')
    # plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False)
    # define some margin (1.05) for the right hand side of the plot
    complete_longest = df_percentage_1.sum(axis=1).max()
    plt.xlim(0, complete_longest)
    ''' Pour effacer l'axe x: '''
    # ax.set(xticklabels=[])
    ''' After a discussion with FSO, we removed the 0-100% horizontal axes on top and below '''
    # Create custom tick positions and labels (from left, 0 to 100%) :
    # xvalues = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    # xlabels = ['{:.0%}'.format(x) for x in xvalues]
    # plt.xticks(xvalues, xlabels)
    # # Create a second x-axis above, with other ticks :
    # ax2 = ax.twiny()
    # ax2.set_xlim(ax.get_xlim())
    # max_of_the_invisible_column = invisible_column.max()
    # ax2.set_xticks([max_of_the_invisible_column + x for x in xvalues])
    # ax2.set_xticklabels(xlabels)
    ''' Instead we center the axis on the middle and define it as zero '''
    potential_xvalues = [longest - 1, longest - 0.8, longest - 0.6, longest - 0.4, longest - 0.2, longest,
                         longest + 0.2, longest + 0.4, longest + 0.6, longest + 0.8, longest + 1]
    potential_xlabels = [100, 80, 60, 40, 20, 0, 20, 40, 60, 80, 100]
    xvalues = []
    xlabels = []
    for index, potential_xvalue in enumerate(potential_xvalues):
        if (potential_xvalue > 0) & (potential_xvalue < complete_longest):
            xvalues.append(potential_xvalue)
            xlabels.append(potential_xlabels[index])
            # plot vertical lines at 0 and 20, -20, 40, -40, etc.
            z = ax.axvline(potential_xvalue, linestyle='-', linewidth=0.5, color='grey', alpha=.5)
            # put this line at the background
            z.set_zorder(-1)
    plt.xticks(xvalues, xlabels)

    # Remove the vertical frame
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # the value of 4000 is particularly chosen for this case
    # xvalues = [longest - 1 + 0.2 * i for i in range(10)]
    # xlabels = ['{:4.0f}'.format(x - longest) for x in xvalues]
    # plt.xticks(xvalues, xlabels)
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            percentage_value = int((round(df_percentage_1.loc[rows][columns] * 100)))
            if percentage_value > 6:
                label = str(percentage_value) + '%'
            else:
                label = str(percentage_value)
            labels.append(label)
    patches = ax.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if 5 <= count_box <= 9:  # corresponds to dark red boxes
                ax.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
            elif 10 <= count_box <= 24:  # corresponds to light colored boxes
                ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            elif count_box >= 15:  # corresponds to dark blue boxes
                ax.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / output_name, bbox_inches='tight')


def visualize_percentage_innovation(df_percentage, output_folder):
    """ Visualize the "innovation" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Innovation_Housing') |
                                        (df_percentage['Variable'] == 'SR_Measure_Innovation_Mobility_costs') |
                                        (df_percentage['Variable'] == 'SR_Measure_Innovation_Autonomous_vehicles') |
                                        (df_percentage['Variable'] == 'SR_Measure_Innovation_Sharing') |
                                        (df_percentage['Variable'] == 'SR_Measure_Innovation_Telecommuting')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Innovation_Housing':
                                                        'Davantage de logements et d???emplois dans les villes et les '
                                                        'agglom??rations\n'
                                                        '(d???o?? une r??duction des distances ?? parcourir)',
                                                    'SR_Measure_Innovation_Mobility_costs':
                                                        'Hausse g??n??rale du co??t de la mobilit?? (voiture et transports '
                                                        'publics)',
                                                    'SR_Measure_Innovation_Autonomous_vehicles':
                                                        'Mesures de soutien pour les v??hicules autonomes\n'
                                                        '(p. ex. modification de lois, exp??riences pilotes)',
                                                    'SR_Measure_Innovation_Sharing':
                                                        'Mesures de soutien pour la mobilit?? partag??e??: '
                                                        'autopartage de type\n'
                                                        'Mobility, covoiturage, syst??mes de pr??t de v??los\n'
                                                        '(p. ex. modification de lois, exp??riences pilotes)',
                                                    'SR_Measure_Innovation_Telecommuting':
                                                        'Soutien aux mod??les de travail flexibles, qui permettent de '
                                                        'r??duire ou\n'
                                                        'de d??caler les d??placements (p. ex. t??l??travail depuis chez soi ou\n'
                                                        'un autre lieu, libre choix des horaires de travail)'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures innovantes dans lesquels des am??liorations sont les plus importantes',
                 horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 10:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_Innovation.png', bbox_inches='tight')


def visualize_percentage_environment(df_percentage, output_folder):
    """ Visualize the "environment" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Environment_Electric_car') |
                                        (df_percentage['Variable'] == 'SR_Measure_Environment_New_vehicles') |
                                        (df_percentage['Variable'] == 'SR_Measure_Environment_Noise') |
                                        (df_percentage['Variable'] == 'SR_Measure_Environment_Traffic_ban') |
                                        (df_percentage['Variable'] == 'SR_Measure_Environment_Fuel_consumption')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Environment_Electric_car':
                                                        'Mesures de soutien pour les v??hicules ??lectriques\n'
                                                        '(p. ex. plus de bornes de recharge, stationnements r??serv??s)',
                                                    'SR_Measure_Environment_New_vehicles':
                                                        'Incitations financi??res ?? l???achat de nouveaux v??hicules\n'
                                                        '??conomes en ??nergie et ?? faibles ??missions',
                                                    'SR_Measure_Environment_Noise':
                                                        'R??duction du bruit du trafic\n'
                                                        '(p. ex. rev??tements anti-bruit, parois anti-bruit)',
                                                    'SR_Measure_Environment_Traffic_ban':
                                                        'Interdiction de circuler en ville pour les voitures\n'
                                                        'd??passant les valeurs limites d?????missions',
                                                    'SR_Measure_Environment_Fuel_consumption':
                                                        'Prescriptions techniques??: limitation de la consommation '
                                                        'de carburant'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle("Mesures li??es ?? l'environnement et l'??nergie dans lesquels des am??liorations sont les plus "
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 10:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_Environment.png', bbox_inches='tight')


def visualize_percentage_walking(df_percentage, output_folder):
    """ Visualize the "walking" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Walking_Zone20') |
                                        (df_percentage['Variable'] == 'SR_Measure_Walking_Safety') |
                                        (df_percentage['Variable'] == 'SR_Measure_Walking_Roadway_design') |
                                        (df_percentage['Variable'] == 'SR_Measure_Walking_Public_space') |
                                        (df_percentage['Variable'] == 'SR_Measure_Walking_Routes')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Walking_Zone20':
                                                        'D??veloppement des zones de rencontre limit??es ?? 20??km/h',
                                                    'SR_Measure_Walking_Safety':
                                                        'Renforcement de la s??curit??\n'
                                                        '(??clairage public, am??lioration de la visibilit??)',
                                                    'SR_Measure_Walking_Roadway_design':
                                                        'R??am??nagement de la voirie\n'
                                                        '(p. ex. ??largissement des trottoirs, zones pi??tonnes)',
                                                    'SR_Measure_Walking_Public_space':
                                                        'Renforcement de la convivialit?? de l???espace public\n'
                                                        '(p. ex. plus de bancs, terrasses de caf??s, espaces verts)',
                                                    'SR_Measure_Walking_Routes':
                                                        'Itin??raires plus directs\n'
                                                        '(p. ex. passerelles pour pi??tons, plus de passages pi??tons)'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures li??es aux am??nagements pi??tons dans lesquels des am??liorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 10:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_Walking.png', bbox_inches='tight')


def visualize_percentage_biking(df_percentage, output_folder):
    """ Visualize the "car" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Biking_Paths') |
                                        (df_percentage['Variable'] == 'SR_Measure_Biking_Lanes') |
                                        (df_percentage['Variable'] == 'SR_Measure_Biking_Parking') |
                                        (df_percentage['Variable'] == 'SR_Measure_Biking_Sharing') |
                                        (df_percentage['Variable'] == 'SR_Measure_Biking_Zone30')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Biking_Paths': 'D??veloppement des pistes cyclables',
                                                    'SR_Measure_Biking_Lanes':
                                                        'D??veloppement des bandes cyclables avec marquage color??',
                                                    'SR_Measure_Biking_Parking':
                                                        'D??veloppement des places de stationnement pour v??los',
                                                    'SR_Measure_Biking_Sharing':
                                                        'D??veloppement des syst??mes de v??los en libre-service',
                                                    'SR_Measure_Biking_Zone30':
                                                        'D??veloppement des zones limit??es ?? 30??km/h'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures li??es aux am??nagements cyclables dans lesquels des am??liorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 9:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_Biking.png', bbox_inches='tight')


def visualize_percentage_public_transport(df_percentage, output_folder):
    """ Visualize the "public transport" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Public_transport_Long_distance') |
                                        (df_percentage['Variable'] == 'SR_Measure_Public_transport_Local') |
                                        (df_percentage['Variable'] == 'SR_Measure_Public_transport_Vehicles') |
                                        (df_percentage['Variable'] == 'SR_Measure_Public_transport_Seats') |
                                        (df_percentage['Variable'] == 'SR_Measure_Public_transport_Comfort')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Public_transport_Long_distance':
                                                        'Am??lioration du trafic longues distances (trains)??:\n'
                                                        'augmentation de la fr??quence ou de la vitesse',
                                                    'SR_Measure_Public_transport_Local':
                                                        'Am??lioration du trafic local et r??gional (RER, tram, bus)??:\n'
                                                        'augmentation de la fr??quence ou de la vitesse',
                                                    'SR_Measure_Public_transport_Vehicles':
                                                        'Modernisation des trains, des bus et des trams\n'
                                                        '(p. ex. nouveaux v??hicules, acc??s Internet)',
                                                    'SR_Measure_Public_transport_Seats':
                                                        'Plus de places sur les lignes existantes',
                                                    'SR_Measure_Public_transport_Comfort':
                                                        'Am??lioration du confort et de l???efficacit?? lors des changements\n'
                                                        '(p. ex. signal??tique, raccourcissement des distances,\n'
                                                        'plus de commerces)'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures li??es aux transports publics dans lesquels des am??liorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 10:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_PT.png', bbox_inches='tight')


def visualize_percentage_car(df_percentage, output_folder):
    """ Visualize the "car" ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Measure_Car_Bottlenecks') |
                                        (df_percentage['Variable'] == 'SR_Measure_Car_Extension') |
                                        (df_percentage['Variable'] == 'SR_Measure_Car_Cities') |
                                        (df_percentage['Variable'] == 'SR_Measure_Car_Safety') |
                                        (df_percentage['Variable'] == 'SR_Measure_Car_Information')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Car_Bottlenecks':
                                                        '??limination des goulets d?????tranglement sur le r??seau existant\n'
                                                        '(p. ex.??construction d???une voie suppl??mentaire sur une '
                                                        'autoroute)',
                                                    'SR_Measure_Car_Extension': 'Extension du r??seau des routes nationales\n'
                                                                                '(p. ex. construction de nouveaux '
                                                                                'tron??ons autoroutiers)',
                                                    'SR_Measure_Car_Cities':
                                                        'Fluidification du trafic dans les villes et les agglom??rations\n'
                                                        '(p. ex. construction de nouveaux contournements,\n'
                                                        'remplacement des feux par des giratoires)',
                                                    'SR_Measure_Car_Safety':
                                                        'Renforcement de la s??curit?? routi??re\n'
                                                        '(p. ex. travaux d???am??nagement, syst??mes d???aide ?? la conduite)',
                                                    'SR_Measure_Car_Information':
                                                        'Diffusion d???informations sur l?????tat du trafic afin d?????viter '
                                                        'les embouteillages\n'
                                                        '(p. ex. via des applications pour smartphones)'},
                                             columns={1: '1e priorit??',
                                                      2: '2e priorit??',
                                                      3: '3e priorit??',
                                                      4: '4e priorit??',
                                                      5: '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures li??es au transport individuel motoris?? dans lesquels des am??liorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 10:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_Car.png', bbox_inches='tight')


def visualize_percentage_general(df_percentage, output_folder):
    """ Visualize the first ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.loc[(df_percentage['Variable'] == 'SR_Sector_Public_transport') |
                                        (df_percentage['Variable'] == 'SR_Sector_Bike') |
                                        (df_percentage['Variable'] == 'SR_Sector_Road') |
                                        (df_percentage['Variable'] == 'SR_Sector_Walk') |
                                        (df_percentage['Variable'] == 'SR_Sector_Environment')].copy()
    df_percentage_1.sort_values(by=['sum_1_2'], inplace=True)
    df_percentage_1.drop(columns=['sum_1_2'], inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Sector_Public_transport':
                                                        'Am??lioration des transports publics (train, bus, tram)',
                                                    'SR_Sector_Bike':
                                                        'Am??lioration des am??nagements cyclables '
                                                        '(y compris v??lo ??lectrique)',
                                                    'SR_Sector_Road':
                                                        'Am??lioration du trafic routier (voiture, moto)',
                                                    'SR_Sector_Walk': 'Am??lioration des am??nagements pi??tons',
                                                    'SR_Sector_Environment':
                                                        'R??duction de l???impact environnemental du trafic'},
                                             columns={'1': '1e priorit??',
                                                      '2': '2e priorit??',
                                                      '3': '3e priorit??',
                                                      '4': '4e priorit??',
                                                      '5': '5e priorit??'})
    # Change the order of the columns
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    print(df_percentage_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229 / 255, 244 / 255, 254 / 255],
                  [172 / 255, 222 / 255, 242 / 255],
                  [0 / 255, 179 / 255, 216 / 255],
                  [0 / 255, 153 / 255, 198 / 255],
                  [0 / 255, 104 / 255, 134 / 255]]
    plot_1 = df_percentage_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Secteurs dans lesquels des am??liorations sont les plus importantes')
    plt.title("Dans l'ordre de la somme des 1e et 2e priorit??s")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_percentage_1:
        for rows in df_percentage_1.index:
            label = str(int((round(df_percentage_1.loc[rows][columns] * 100))))
            labels.append(label)
    patches = plot_1.patches
    count_box = 0
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            if count_box <= 9:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center')
            else:
                plot_1.text(x + width / 2., y + height / 2., label, ha='center', va='center', color='w')
        count_box += 1
    fig.savefig(output_folder / 'Stated_Ranking_General.png', bbox_inches='tight')


def remove_partial_answers(df_modul3):
    # Remove answers with -99 somewhere in the 5 answers
    list_of_questions_sector = ['SR_Sector_Public_transport',
                                'SR_Sector_Bike',
                                'SR_Sector_Road',
                                'SR_Sector_Walk',
                                'SR_Sector_Environment']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_sector)
    list_of_questions_measure_car = ['SR_Measure_Car_Bottlenecks',
                                     'SR_Measure_Car_Extension',
                                     'SR_Measure_Car_Cities',
                                     'SR_Measure_Car_Safety',
                                     'SR_Measure_Car_Information']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_car)
    list_of_questions_measure_public_transport = ['SR_Measure_Public_transport_Long_distance',
                                                  'SR_Measure_Public_transport_Local',
                                                  'SR_Measure_Public_transport_Vehicles',
                                                  'SR_Measure_Public_transport_Seats',
                                                  'SR_Measure_Public_transport_Comfort']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_public_transport)
    list_of_questions_measure_biking = ['SR_Measure_Biking_Paths',
                                        'SR_Measure_Biking_Lanes',
                                        'SR_Measure_Biking_Parking',
                                        'SR_Measure_Biking_Sharing',
                                        'SR_Measure_Biking_Zone30']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_biking)
    list_of_questions_measure_walking = ['SR_Measure_Walking_Zone20',
                                         'SR_Measure_Walking_Safety',
                                         'SR_Measure_Walking_Roadway_design',
                                         'SR_Measure_Walking_Public_space',
                                         'SR_Measure_Walking_Routes']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_walking)
    list_of_questions_measure_environment = ['SR_Measure_Environment_Electric_car',
                                             'SR_Measure_Environment_New_vehicles',
                                             'SR_Measure_Environment_Noise',
                                             'SR_Measure_Environment_Traffic_ban',
                                             'SR_Measure_Environment_Fuel_consumption']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_environment)
    list_of_questions_measure_innovation = ['SR_Measure_Innovation_Housing',
                                            'SR_Measure_Innovation_Mobility_costs',
                                            'SR_Measure_Innovation_Autonomous_vehicles',
                                            'SR_Measure_Innovation_Sharing',
                                            'SR_Measure_Innovation_Telecommuting']
    df_modul3 = remove_partial_answers_for_list(df_modul3, list_of_questions_measure_innovation)

    # Remove answers that are not exactly 1, 2, 3, 4, 5 (e.g. 1, 1, 1, 1, 1)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_sector)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_car)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_public_transport)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_biking)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_walking)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_environment)
    df_modul3 = remove_wrong_answers_for_list(df_modul3, list_of_questions_measure_innovation)
    return df_modul3


def remove_wrong_answers_for_list(df_modul3, list_of_question_numbers):
    for ranking in [1, 2, 3, 4, 5]:
        df_modul3['at_least_one'] = False
        # Check that there is at least one 1 (or 2, or...)
        for question_number in list_of_question_numbers:
            df_modul3.loc[df_modul3[str(question_number)] == ranking, 'at_least_one'] = True
        for question_number in list_of_question_numbers:
            df_modul3.loc[~df_modul3['at_least_one'], str(question_number)] = -99
    del df_modul3['at_least_one']
    return df_modul3


def remove_partial_answers_for_list(df_modul3, list_of_question_numbers):
    for questions1 in list_of_question_numbers:
        for questions2 in list_of_question_numbers:
            if questions1 != questions2:
                df_modul3.loc[df_modul3[questions1] == -99, questions2] = -99
                df_modul3.loc[df_modul3[questions1] == -99, questions2] = -99
                df_modul3.loc[df_modul3[questions1] == -99, questions2] = -99
                df_modul3.loc[df_modul3[questions1] == -99, questions2] = -99
    return df_modul3
