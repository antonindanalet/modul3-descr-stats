import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def descr_stats(df_module_3):
    df_module_3 = remove_partial_answers(df_module_3)
    df_module_3 = remove_respondents_without_mobility_data(df_module_3)
    df_module_3 = remove_respondents_without_weights(df_module_3)
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

    # Compute weighted average and confidence interval for each group of questions
    df_for_csv = pd.DataFrame(columns=['Variable',
                                       '1', '1 (+/-)',
                                       '2', '2 (+/-)',
                                       '3', '3 (+/-)',
                                       '4', '4 (+/-)',
                                       '5', '5 (+/-)',
                                       'Sample'])
    for question in list_of_questions:
        list_of_questions_with_ranking = [question + '_' + str(i) for i in range(1, 6)]
        df_module_3_with_answers = df_module_3[df_module_3[list_of_questions_with_ranking[0][:-2]] != -99]
        percentage_and_sample = get_weighted_avg_and_std(df_module_3_with_answers, weights='WP', percentage=True,
                                                         list_of_columns=list_of_questions_with_ranking)
        dict_percentage = percentage_and_sample[0]
        sample = percentage_and_sample[1]
        list_of_values_for_row = [question]
        for i in range(1, 6):
            list_of_values_for_row.append(dict_percentage[question + '_' + str(i)][0])
            list_of_values_for_row.append(dict_percentage[question + '_' + str(i)][1])
        list_of_values_for_row.append(sample)
        df_for_csv.loc[len(df_for_csv.index)] = list_of_values_for_row
    output_folder = Path("../data/output/table/")
    df_for_csv.to_csv(output_folder / 'module_3_results.csv', index=False, sep=';')
    return df_for_csv


def remove_respondents_without_weights(df_module_3):
    """ These people don't have weights / HHNR and do not exist in the other datafiles from FSO. """
    df_module_3 = df_module_3[df_module_3['username'] != '70691']
    df_module_3 = df_module_3[df_module_3['username'] != '78742']
    return df_module_3


def remove_respondents_without_mobility_data(df_modul3):
    df_modul3 = df_modul3[df_modul3['with_mobility_data'] == True]
    return df_modul3


def visualize_percentage(df_percentage):
    """ This functions generates two types of graphical representations of the ranking questions. """
    ''' Visualize as bar plot '''
    output_folder = Path("../data/output/bar_plot/")
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_percentage['sum_1_2'] = df_percentage['1'] + df_percentage['2']
    # visualize_percentage_general(df_percentage, output_folder)
    # visualize_percentage_car(df_percentage, output_folder)
    # visualize_percentage_public_transport(df_percentage, output_folder)
    # visualize_percentage_biking(df_percentage, output_folder)
    # visualize_percentage_walking(df_percentage, output_folder)
    # visualize_percentage_environment(df_percentage, output_folder)
    # visualize_percentage_innovation(df_percentage, output_folder)
    ''' Visualize as divergent bar plot '''
    output_folder = Path("../data/output/divergent_bar_plot/")
    # General
    title = 'Secteurs dans lesquels des améliorations sont les plus importantes'
    dict_measures = {'SR_Sector_Public_transport': 'Amélioration des transports publics (train, bus, tram)',
                     'SR_Sector_Bike': 'Amélioration des aménagements cyclables (y compris vélo électrique)',
                     'SR_Sector_Road': 'Amélioration du trafic routier (voiture, moto)',
                     'SR_Sector_Walk': 'Amélioration des aménagements piétons',
                     'SR_Sector_Environment': 'Réduction de l’impact environnemental du trafic'}
    output_name = 'Stated_Ranking_General.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Car
    title = 'Mesures liées au transport individuel motorisé dans lesquels des améliorations sont les plus importantes'
    dict_measures = {'SR_Measure_Car_Bottlenecks': 'Élimination des goulets d’étranglement sur le réseau existant\n'
                                                   '(p. ex. construction d’une voie supplémentaire sur une '
                                                   'autoroute)',
                     'SR_Measure_Car_Extension': 'Extension du réseau des routes nationales\n'
                                                 '(p. ex. construction de nouveaux tronçons autoroutiers)',
                     'SR_Measure_Car_Cities': 'Fluidification du trafic dans les villes et les agglomérations\n'
                                              '(p. ex. construction de nouveaux contournements,\n'
                                              'remplacement des feux par des giratoires)',
                     'SR_Measure_Car_Safety': 'Renforcement de la sécurité routière\n'
                                              '(p. ex. travaux d’aménagement, systèmes d’aide à la conduite)',
                     'SR_Measure_Car_Information': 'Diffusion d’informations sur l’état du trafic afin d’éviter les '
                                                   'embouteillages\n'
                                                   '(p. ex. via des applications pour smartphones)'}
    output_name = 'Stated_Ranking_Car.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Public transport
    title = 'Mesures liées aux transports publics dans lesquels des améliorations sont les plus importantes'
    dict_measures = {'SR_Measure_Public_transport_Long_distance': 'Amélioration du trafic longues distances '
                                                                  '(trains) :\n'
                                                                  'augmentation de la fréquence ou de la vitesse',
                     'SR_Measure_Public_transport_Local': 'Amélioration du trafic local et régional (RER, tram, '
                                                          'bus) :\n'
                                                          'augmentation de la fréquence ou de la vitesse',
                     'SR_Measure_Public_transport_Vehicles': 'Modernisation des trains, des bus et des trams\n'
                                                             '(p. ex. nouveaux véhicules, accès Internet)',
                     'SR_Measure_Public_transport_Seats': 'Plus de places sur les lignes existantes',
                     'SR_Measure_Public_transport_Comfort': 'Amélioration du confort et de l’efficacité lors des '
                                                            'changements\n'
                                                            '(p. ex. signalétique, raccourcissement des distances,\n'
                                                            'plus de commerces)'}
    output_name = 'Stated_Ranking_PT.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Biking
    title = 'Mesures liées aux aménagements cyclables dans lesquels des améliorations sont les plus importantes'
    dict_measures = {'SR_Measure_Biking_Paths': 'Développement des pistes cyclables',
                     'SR_Measure_Biking_Lanes': 'Développement des bandes cyclables avec marquage coloré',
                     'SR_Measure_Biking_Parking': 'Développement des places de stationnement pour vélos',
                     'SR_Measure_Biking_Sharing': 'Développement des systèmes de vélos en libre-service',
                     'SR_Measure_Biking_Zone30': 'Développement des zones limitées à 30 km/h'}
    output_name = 'Stated_Ranking_Biking.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Walking
    title = 'Mesures liées aux aménagements piétons dans lesquels des améliorations sont les plus importantes'
    dict_measures = {'SR_Measure_Walking_Zone20': 'Développement des zones de rencontre limitées à 20 km/h',
                     'SR_Measure_Walking_Safety': 'Renforcement de la sécurité\n'
                                                  '(éclairage public, amélioration de la visibilité)',
                     'SR_Measure_Walking_Roadway_design': 'Réaménagement de la voirie\n'
                                                          '(p. ex. élargissement des trottoirs, zones piétonnes)',
                     'SR_Measure_Walking_Public_space': 'Renforcement de la convivialité de l’espace public\n'
                                                        '(p. ex. plus de bancs, terrasses de cafés, espaces verts)',
                     'SR_Measure_Walking_Routes': 'Itinéraires plus directs\n'
                                                  '(p. ex. passerelles pour piétons, plus de passages piétons)'}
    output_name = 'Stated_Ranking_Walking.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Environment
    title = "Mesures liées à l'environnement et l'énergie dans lesquels des améliorations sont les plus importantes"
    dict_measures = {'SR_Measure_Environment_Electric_car': 'Mesures de soutien pour les véhicules électriques\n'
                                                            '(p. ex. plus de bornes de recharge, stationnements réservés)',
                     'SR_Measure_Environment_New_vehicles': 'Incitations financières à l’achat de nouveaux véhicules\n'
                                                            'économes en énergie et à faibles émissions',
                     'SR_Measure_Environment_Noise': 'Réduction du bruit du trafic\n'
                                                     '(p. ex. revêtements anti-bruit, parois anti-bruit)',
                     'SR_Measure_Environment_Traffic_ban': 'Interdiction de circuler en ville pour les voitures\n'
                                                           'dépassant les valeurs limites d’émissions',
                     'SR_Measure_Environment_Fuel_consumption': 'Prescriptions techniques :'
                                                                'limitation de la consommation de carburant'}
    output_name = 'Stated_Ranking_Environment.png'
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name)
    # Innovation
    title = "Mesures innovantes dans lesquels des améliorations sont les plus importantes"
    dict_measures = {'SR_Measure_Innovation_Housing': 'Davantage de logements et d’emplois dans les villes et les '
                                                      'agglomérations\n'
                                                      '(d’où une réduction des distances à parcourir)',
                     'SR_Measure_Innovation_Mobility_costs': 'Hausse générale du coût de la mobilité '
                                                             '(voiture et transports publics)',
                     'SR_Measure_Innovation_Autonomous_vehicles': 'Mesures de soutien pour les véhicules autonomes\n'
                                                                  '(p. ex. modification de lois, expériences pilotes)',
                     'SR_Measure_Innovation_Sharing': 'Mesures de soutien pour la mobilité partagée : '
                                                      'autopartage de type\n'
                                                      'Mobility, covoiturage, systèmes de prêt de vélos\n'
                                                      '(p. ex. modification de lois, expériences pilotes)',
                     'SR_Measure_Innovation_Telecommuting': 'Soutien aux modèles de travail flexibles, qui permettent '
                                                            'de réduire ou\n'
                                                            'de décaler les déplacements (p. ex. télétravail depuis '
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
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
                                             columns={1: '$\mathregular{1^{re}}$ priorité',
                                                      2: '$\mathregular{2^e}$ priorité',
                                                      3: '$\mathregular{3^e}$ priorité',
                                                      4: '$\mathregular{4^e}$ priorité',
                                                      5: '$\mathregular{5^e}$ priorité',
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
    # plt.suptitle('Secteurs dans lesquels des améliorations sont les plus importantes')
    # plt.title("Dans l'ordre de la somme des 1e et 2e priorités")
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Innovation_Housing':
                                                        'Davantage de logements et d’emplois dans les villes et les '
                                                        'agglomérations\n'
                                                        '(d’où une réduction des distances à parcourir)',
                                                    'SR_Measure_Innovation_Mobility_costs':
                                                        'Hausse générale du coût de la mobilité (voiture et transports '
                                                        'publics)',
                                                    'SR_Measure_Innovation_Autonomous_vehicles':
                                                        'Mesures de soutien pour les véhicules autonomes\n'
                                                        '(p. ex. modification de lois, expériences pilotes)',
                                                    'SR_Measure_Innovation_Sharing':
                                                        'Mesures de soutien pour la mobilité partagée : '
                                                        'autopartage de type\n'
                                                        'Mobility, covoiturage, systèmes de prêt de vélos\n'
                                                        '(p. ex. modification de lois, expériences pilotes)',
                                                    'SR_Measure_Innovation_Telecommuting':
                                                        'Soutien aux modèles de travail flexibles, qui permettent de '
                                                        'réduire ou\n'
                                                        'de décaler les déplacements (p. ex. télétravail depuis chez soi ou\n'
                                                        'un autre lieu, libre choix des horaires de travail)'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle('Mesures innovantes dans lesquels des améliorations sont les plus importantes',
                 horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Environment_Electric_car':
                                                        'Mesures de soutien pour les véhicules électriques\n'
                                                        '(p. ex. plus de bornes de recharge, stationnements réservés)',
                                                    'SR_Measure_Environment_New_vehicles':
                                                        'Incitations financières à l’achat de nouveaux véhicules\n'
                                                        'économes en énergie et à faibles émissions',
                                                    'SR_Measure_Environment_Noise':
                                                        'Réduction du bruit du trafic\n'
                                                        '(p. ex. revêtements anti-bruit, parois anti-bruit)',
                                                    'SR_Measure_Environment_Traffic_ban':
                                                        'Interdiction de circuler en ville pour les voitures\n'
                                                        'dépassant les valeurs limites d’émissions',
                                                    'SR_Measure_Environment_Fuel_consumption':
                                                        'Prescriptions techniques : limitation de la consommation '
                                                        'de carburant'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle("Mesures liées à l'environnement et l'énergie dans lesquels des améliorations sont les plus "
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Walking_Zone20':
                                                        'Développement des zones de rencontre limitées à 20 km/h',
                                                    'SR_Measure_Walking_Safety':
                                                        'Renforcement de la sécurité\n'
                                                        '(éclairage public, amélioration de la visibilité)',
                                                    'SR_Measure_Walking_Roadway_design':
                                                        'Réaménagement de la voirie\n'
                                                        '(p. ex. élargissement des trottoirs, zones piétonnes)',
                                                    'SR_Measure_Walking_Public_space':
                                                        'Renforcement de la convivialité de l’espace public\n'
                                                        '(p. ex. plus de bancs, terrasses de cafés, espaces verts)',
                                                    'SR_Measure_Walking_Routes':
                                                        'Itinéraires plus directs\n'
                                                        '(p. ex. passerelles pour piétons, plus de passages piétons)'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle('Mesures liées aux aménagements piétons dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Biking_Paths': 'Développement des pistes cyclables',
                                                    'SR_Measure_Biking_Lanes':
                                                        'Développement des bandes cyclables avec marquage coloré',
                                                    'SR_Measure_Biking_Parking':
                                                        'Développement des places de stationnement pour vélos',
                                                    'SR_Measure_Biking_Sharing':
                                                        'Développement des systèmes de vélos en libre-service',
                                                    'SR_Measure_Biking_Zone30':
                                                        'Développement des zones limitées à 30 km/h'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle('Mesures liées aux aménagements cyclables dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Public_transport_Long_distance':
                                                        'Amélioration du trafic longues distances (trains) :\n'
                                                        'augmentation de la fréquence ou de la vitesse',
                                                    'SR_Measure_Public_transport_Local':
                                                        'Amélioration du trafic local et régional (RER, tram, bus) :\n'
                                                        'augmentation de la fréquence ou de la vitesse',
                                                    'SR_Measure_Public_transport_Vehicles':
                                                        'Modernisation des trains, des bus et des trams\n'
                                                        '(p. ex. nouveaux véhicules, accès Internet)',
                                                    'SR_Measure_Public_transport_Seats':
                                                        'Plus de places sur les lignes existantes',
                                                    'SR_Measure_Public_transport_Comfort':
                                                        'Amélioration du confort et de l’efficacité lors des changements\n'
                                                        '(p. ex. signalétique, raccourcissement des distances,\n'
                                                        'plus de commerces)'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle('Mesures liées aux transports publics dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Measure_Car_Bottlenecks':
                                                        'Élimination des goulets d’étranglement sur le réseau existant\n'
                                                        '(p. ex. construction d’une voie supplémentaire sur une '
                                                        'autoroute)',
                                                    'SR_Measure_Car_Extension': 'Extension du réseau des routes nationales\n'
                                                                                '(p. ex. construction de nouveaux '
                                                                                'tronçons autoroutiers)',
                                                    'SR_Measure_Car_Cities':
                                                        'Fluidification du trafic dans les villes et les agglomérations\n'
                                                        '(p. ex. construction de nouveaux contournements,\n'
                                                        'remplacement des feux par des giratoires)',
                                                    'SR_Measure_Car_Safety':
                                                        'Renforcement de la sécurité routière\n'
                                                        '(p. ex. travaux d’aménagement, systèmes d’aide à la conduite)',
                                                    'SR_Measure_Car_Information':
                                                        'Diffusion d’informations sur l’état du trafic afin d’éviter '
                                                        'les embouteillages\n'
                                                        '(p. ex. via des applications pour smartphones)'},
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité'})
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
    plt.suptitle('Mesures liées au transport individuel motorisé dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
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
    df_percentage_1.drop(columns=['sum_1_2', 'Sample', '1 (+/-)', '2 (+/-)', '3 (+/-)', '4 (+/-)', '5 (+/-)'],
                         inplace=True)
    df_percentage_1.set_index('Variable', inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={'SR_Sector_Public_transport':
                                                        'Amélioration des transports publics (train, bus, tram)',
                                                    'SR_Sector_Bike':
                                                        'Amélioration des aménagements cyclables '
                                                        '(y compris vélo électrique)',
                                                    'SR_Sector_Road':
                                                        'Amélioration du trafic routier (voiture, moto)',
                                                    'SR_Sector_Walk': 'Amélioration des aménagements piétons',
                                                    'SR_Sector_Environment':
                                                        'Réduction de l’impact environnemental du trafic'},
                                             columns={'1': '1e priorité',
                                                      '2': '2e priorité',
                                                      '3': '3e priorité',
                                                      '4': '4e priorité',
                                                      '5': '5e priorité'})
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
    plt.suptitle('Secteurs dans lesquels des améliorations sont les plus importantes')
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités")
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
