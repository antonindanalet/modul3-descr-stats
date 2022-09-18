import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt


def descr_stats(df_modul3, date_of_delivery):
    df_count = count_values(df_modul3)
    df_percentage = count2percentage(df_count)
    visualize_percentage(df_percentage, date_of_delivery)


def visualize_percentage(df_percentage, date_of_delivery):
    """ This functions generates two types of graphical representations of the ranking questions. """
    ''' Visualize as bar plot '''
    output_folder = Path("../data/output/bar_plot/")
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
    title = 'Secteurs dans lesquels des améliorations sont les plus importantes'
    dict_measures = {101: 'Amélioration des transports publics (train, bus, tram)',
                     102: 'Amélioration des aménagements cyclables (y compris vélo électrique)',
                     103: 'Amélioration du trafic routier (voiture, moto)',
                     104: 'Amélioration des aménagements piétons',
                     105: 'Réduction de l’impact environnemental du trafic'}
    output_name = 'Stated_Ranking_General_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 0
    location_in_df_percentage_end = 5
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Car
    title = 'Mesures liées au transport individuel motorisé dans lesquels des améliorations sont les plus importantes'
    dict_measures = {211: 'Élimination des goulets d’étranglement sur le réseau existant\n'
                          '(p. ex. construction d’une voie supplémentaire sur une autoroute)',
                     212: 'Extension du réseau des routes nationales\n'
                          '(p. ex. construction de nouveaux tronçons autoroutiers)',
                     213: 'Fluidification du trafic dans les villes et les agglomérations\n'
                          '(p. ex. construction de nouveaux contournements,\n'
                          'remplacement des feux par des giratoires)',
                     214: 'Renforcement de la sécurité routière\n'
                          '(p. ex. travaux d’aménagement, systèmes d’aide à la conduite)',
                     215: 'Diffusion d’informations sur l’état du trafic afin d’éviter les '
                          'embouteillages\n(p. ex. via des applications pour smartphones)'}
    output_name = 'Stated_Ranking_Car_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 5
    location_in_df_percentage_end = 10
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Public transport
    title = 'Mesures liées aux transports publics dans lesquels des améliorations sont les plus importantes'
    dict_measures = {221: 'Amélioration du trafic longues distances (trains) :\n'
                          'augmentation de la fréquence ou de la vitesse',
                     222: 'Amélioration du trafic local et régional (RER, tram, bus) :\n'
                          'augmentation de la fréquence ou de la vitesse',
                     223: 'Modernisation des trains, des bus et des trams\n'
                          '(p. ex. nouveaux véhicules, accès Internet)',
                     224: 'Plus de places sur les lignes existantes',
                     225: 'Amélioration du confort et de l’efficacité lors des changements\n'
                          '(p. ex. signalétique, raccourcissement des distances,\n'
                          'plus de commerces)'}
    output_name = 'Stated_Ranking_PT_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 10
    location_in_df_percentage_end = 15
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Biking
    title = 'Mesures liées aux aménagements cyclables dans lesquels des améliorations sont les plus importantes'
    dict_measures = {231: 'Développement des pistes cyclables',
                     232: 'Développement des bandes cyclables avec marquage coloré',
                     233: 'Développement des places de stationnement pour vélos',
                     234: 'Développement des systèmes de vélos en libre-service',
                     235: 'Développement des zones limitées à 30 km/h'}
    output_name = 'Stated_Ranking_Biking_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 15
    location_in_df_percentage_end = 20
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Walking
    title = 'Mesures liées aux aménagements piétons dans lesquels des améliorations sont les plus importantes'
    dict_measures = {241: 'Développement des zones de rencontre limitées à 20 km/h',
                     242: 'Renforcement de la sécurité\n'
                          '(éclairage public, amélioration de la visibilité)',
                     243: 'Réaménagement de la voirie\n'
                          '(p. ex. élargissement des trottoirs, zones piétonnes)',
                     244: 'Renforcement de la convivialité de l’espace public\n'
                          '(p. ex. plus de bancs, terrasses de cafés, espaces verts)',
                     245: 'Itinéraires plus directs\n'
                          '(p. ex. passerelles pour piétons, plus de passages piétons)'}
    output_name = 'Stated_Ranking_Walking_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 20
    location_in_df_percentage_end = 25
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Environment
    title = "Mesures liées à l'environnement et l'énergie dans lesquels des améliorations sont les plus importantes"
    dict_measures = {251: 'Mesures de soutien pour les véhicules électriques\n'
                          '(p. ex. plus de bornes de recharge, stationnements réservés)',
                     252: 'Incitations financières à l’achat de nouveaux véhicules\n'
                          'économes en énergie et à faibles émissions',
                     253: 'Réduction du bruit du trafic\n'
                          '(p. ex. revêtements anti-bruit, parois anti-bruit)',
                     254: 'Interdiction de circuler en ville pour les voitures\n'
                          'dépassant les valeurs limites d’émissions',
                     255: 'Prescriptions techniques : limitation de la consommation de carburant'}
    output_name = 'Stated_Ranking_Environment_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 25
    location_in_df_percentage_end = 30
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)
    # Innovation
    title = "Mesures innovantes dans lesquels des améliorations sont les plus importantes"
    dict_measures = {401: 'Davantage de logements et d’emplois dans les villes et les agglomérations\n'
                          '(d’où une réduction des distances à parcourir)',
                     402: 'Hausse générale du coût de la mobilité (voiture et transports publics)',
                     403: 'Mesures de soutien pour les véhicules autonomes\n'
                          '(p. ex. modification de lois, expériences pilotes)',
                     404: 'Mesures de soutien pour la mobilité partagée : autopartage de type\n'
                          'Mobility, covoiturage, systèmes de prêt de vélos\n'
                          '(p. ex. modification de lois, expériences pilotes)',
                     405: 'Soutien aux modèles de travail flexibles, qui permettent de réduire ou\n'
                          'de décaler les déplacements (p. ex. télétravail depuis chez soi ou\n'
                          'un autre lieu, libre choix des horaires de travail)'}
    output_name = 'Stated_Ranking_Innovation_' + date_of_delivery + '.png'
    location_in_df_percentage_beginning = 30
    location_in_df_percentage_end = 35
    visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end)


def visualize_percentage_divergent(df_percentage, output_folder, title, dict_measures, output_name,
                                   location_in_df_percentage_beginning, location_in_df_percentage_end):
    """ Visualize the first ranking questions """
    # Filter the count results of the first question
    df_percentage_1 = df_percentage.iloc[location_in_df_percentage_beginning:location_in_df_percentage_end].copy()
    # Change the order of the columns tp have priority 1 on the right
    df_percentage_1 = df_percentage_1.sort_index(axis=1, ascending=False)
    ''' Define the ranking of measures '''
    # Inspiration for the code:
    # https://stackoverflow.com/questions/23142358/create-a-diverging-stacked-bar-chart-in-matplotlib
    # https://blog.orikami.nl/behind-the-screens-likert-scale-visualization-368557ad72d1
    # Define the middle point of the measures by summing prio 4 & 5 plus half of prio 3
    middles = df_percentage_1[[5, 4]].sum(axis=1) + df_percentage_1[3] * .5
    longest = middles.max()
    # Insert an invisible column in the dataframe
    invisible_column = (middles - longest).abs()
    df_percentage_1.insert(0, '', invisible_column)
    # Change the order of the rankings, based on the middle point
    df_percentage_1.sort_values(by=[''], inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index=dict_measures,
                                             columns={1: '1e priorité',
                                                      2: '2e priorité',
                                                      3: '3e priorité',
                                                      4: '4e priorité',
                                                      5: '5e priorité',
                                                      '': ''})
    # Plot the answers
    sns.set_style("whitegrid", {'axes.grid': False})
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    # Define the color scheme of the Federal Statistical Office (FSO),
    # with white as the first color, for the invisible column
    FSO_colors = [[1, 1, 1],  # white
                  [232/255, 89/255, 29/255],  # dark red
                  [245/255, 164/255, 40/255],  # light red
                  [207/255, 208/255, 208/255],  # grey
                  [177/255, 222/255, 241/255],  # light blue
                  [24/255, 154/255, 196/255]]  # dark blue
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
    df_count_1 = df_percentage.iloc[30:35].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={401: 'Davantage de logements et d’emplois dans les villes et les '
                                               'agglomérations\n'
                                               '(d’où une réduction des distances à parcourir)',
                                          402: 'Hausse générale du coût de la mobilité (voiture et transports publics)',
                                          403: 'Mesures de soutien pour les véhicules autonomes\n'
                                               '(p. ex. modification de lois, expériences pilotes)',
                                          404: 'Mesures de soutien pour la mobilité partagée : autopartage de type\n'
                                               'Mobility, covoiturage, systèmes de prêt de vélos\n'
                                               '(p. ex. modification de lois, expériences pilotes)',
                                          405: 'Soutien aux modèles de travail flexibles, '
                                               'qui permettent de réduire ou\n'
                                               'de décaler les déplacements (p. ex. télétravail depuis chez soi ou\n'
                                               'un autre lieu, libre choix des horaires de travail)'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures innovantes dans lesquels des améliorations sont les plus importantes',
                 horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    """ Visualize the "walking" ranking questions """
    # Filter the count results of the first question
    df_count_1 = df_percentage.iloc[25:30].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={251: 'Mesures de soutien pour les véhicules électriques\n'
                                               '(p. ex. plus de bornes de recharge, stationnements réservés)',
                                          252: 'Incitations financières à l’achat de nouveaux véhicules\n'
                                               'économes en énergie et à faibles émissions',
                                          253: 'Réduction du bruit du trafic\n'
                                               '(p. ex. revêtements anti-bruit, parois anti-bruit)',
                                          254: 'Interdiction de circuler en ville pour les voitures\n'
                                               'dépassant les valeurs limites d’émissions',
                                          255: 'Prescriptions techniques : limitation de la consommation de carburant'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle("Mesures liées à l'environnement et l'énergie dans lesquels des améliorations sont les plus "
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    df_count_1 = df_percentage.iloc[20:25].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={241: 'Développement des zones de rencontre limitées à 20 km/h',
                                          242: 'Renforcement de la sécurité\n'
                                               '(éclairage public, amélioration de la visibilité)',
                                          243: 'Réaménagement de la voirie\n'
                                               '(p. ex. élargissement des trottoirs, zones piétonnes)',
                                          244: 'Renforcement de la convivialité de l’espace public\n'
                                               '(p. ex. plus de bancs, terrasses de cafés, espaces verts)',
                                          245: 'Itinéraires plus directs\n'
                                               '(p. ex. passerelles pour piétons, plus de passages piétons)'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures liées aux aménagements piétons dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    df_count_1 = df_percentage.iloc[15:20].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={231: 'Développement des pistes cyclables',
                                          232: 'Développement des bandes cyclables avec marquage coloré',
                                          233: 'Développement des places de stationnement pour vélos',
                                          234: 'Développement des systèmes de vélos en libre-service',
                                          235: 'Développement des zones limitées à 30 km/h'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures liées aux aménagements cyclables dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, frameon=False)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    """ Visualize the "car" ranking questions """
    # Filter the count results of the first question
    df_count_1 = df_percentage.iloc[10:15].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={221: 'Amélioration du trafic longues distances (trains) :\n'
                                               'augmentation de la fréquence ou de la vitesse',
                                          222: 'Amélioration du trafic local et régional (RER, tram, bus) :\n'
                                               'augmentation de la fréquence ou de la vitesse',
                                          223: 'Modernisation des trains, des bus et des trams\n'
                                               '(p. ex. nouveaux véhicules, accès Internet)',
                                          224: 'Plus de places sur les lignes existantes',
                                          225: 'Amélioration du confort et de l’efficacité lors des changements\n'
                                               '(p. ex. signalétique, raccourcissement des distances,\n'
                                               'plus de commerces)'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures liées aux transports publics dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    df_count_1 = df_percentage.iloc[5:10].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_count_1['sum'] = df_count_1[1] + df_count_1[2]
    df_count_1.sort_values(by=['sum'], inplace=True)
    df_count_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_count_1 = df_count_1.rename(index={211: 'Élimination des goulets d’étranglement sur le réseau existant\n'
                                               '(p. ex. construction d’une voie supplémentaire sur une autoroute)',
                                          212: 'Extension du réseau des routes nationales\n'
                                               '(p. ex. construction de nouveaux tronçons autoroutiers)',
                                          213: 'Fluidification du trafic dans les villes et les agglomérations\n'
                                               '(p. ex. construction de nouveaux contournements,\n'
                                               'remplacement des feux par des giratoires)',
                                          214: 'Renforcement de la sécurité routière\n'
                                               '(p. ex. travaux d’aménagement, systèmes d’aide à la conduite)',
                                          215: 'Diffusion d’informations sur l’état du trafic afin d’éviter les '
                                               'embouteillages\n(p. ex. via des applications pour smartphones)'},
                                   columns={1: '1e priorité',
                                            2: '2e priorité',
                                            3: '3e priorité',
                                            4: '4e priorité',
                                            5: '5e priorité'})
    # Change the order of the columns
    df_count_1 = df_count_1.sort_index(axis=1, ascending=False)
    print(df_count_1)
    # Plot the answers
    sns.set(style="whitegrid")
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(25, 15))
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
    plot_1 = df_count_1.plot(kind='barh', stacked=True, color=FSO_colors)
    fig = plot_1.get_figure()
    plt.suptitle('Mesures liées au transport individuel motorisé dans lesquels des améliorations sont les plus '
                 'importantes', horizontalalignment='left', x=-0.5)
    plt.title("Dans l'ordre de la somme des 1e et 2e priorités", horizontalalignment='center', loc='center')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.xlim([0, 1])
    # Add the values in the bars
    labels = []
    for columns in df_count_1:
        for rows in df_count_1.index:
            label = str(int((round(df_count_1.loc[rows][columns] * 100))))
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
    df_percentage_1 = df_percentage.iloc[0:5].copy()
    # Change the order of the rankings, based on the sum of prio 1 and 2
    df_percentage_1['sum'] = df_percentage_1[1] + df_percentage_1[2]
    df_percentage_1.sort_values(by=['sum'], inplace=True)
    df_percentage_1.drop(columns=['sum'], inplace=True)
    # Rename the columns and index
    df_percentage_1 = df_percentage_1.rename(index={101: 'Amélioration des transports publics (train, bus, tram)',
                                                    102: 'Amélioration des aménagements cyclables (y compris vélo '
                                                         'électrique)',
                                                    103: 'Amélioration du trafic routier (voiture, moto)',
                                                    104: 'Amélioration des aménagements piétons',
                                                    105: 'Réduction de l’impact environnemental du trafic'},
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
    FSO_colors = [[229/255, 244/255, 254/255],
                  [172/255, 222/255, 242/255],
                  [0/255, 179/255, 216/255],
                  [0/255, 153/255, 198/255],
                  [0/255, 104/255, 134/255]]
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


def count2percentage(df_modul3):
    df_modul3['sum'] = df_modul3[1] + df_modul3[2] + df_modul3[3] + df_modul3[4] + df_modul3[5]
    for i in range(1, 6):
        df_modul3[i] = df_modul3[i] / df_modul3['sum']
    df_modul3.drop(columns=['sum'], inplace=True)
    return df_modul3


def count_values(df_modul3):
    df_count = pd.DataFrame(0, index=[101, 102, 103, 104, 105,
                                      211, 212, 213, 214, 215,
                                      221, 222, 223, 224, 225,
                                      231, 232, 233, 234, 235,
                                      241, 242, 243, 244, 245,
                                      251, 252, 253, 254, 255,
                                      401, 402, 403, 404, 405], columns=[1, 2, 3, 4, 5])
    for columns_stated_ranking in df_modul3.columns:
        if columns_stated_ranking.startswith('lpRang_v'):
            question_number = int(columns_stated_ranking[-8:-5])
            counts = df_modul3[columns_stated_ranking].value_counts(sort=False)
            for value, count in counts.iteritems():
                if value != -99:
                    df_count.at[question_number, int(value)] = df_count.at[question_number, int(value)] + count
    return df_count
