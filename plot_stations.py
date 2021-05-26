import numpy as np
import pygmt
import pandas as pd
np.random.seed(45)  # to get the same color at each run


def plot_stations():
    df = pd.read_csv('station_info.txt', delimiter='|')
    print(df.head())

    # get the list of networks
    networks = list(set(df['#Network'].tolist()))

    dfs = []
    for net in networks:
        df1 = df[df['#Network'] == net]
        dfs.append(df1)

    colorsList = []
    for i in range(len(networks)):
        colorsList.append('#%06X' % np.random.randint(0, 0xFFFFFF))

    minlon, maxlon = df['Longitude'].min()-1, df['Longitude'].max()+1
    minlat, maxlat = df['Latitude'].min()-1, df['Latitude'].max()+1

    # define etopo data file

    topo_data = "@earth_relief_30s"

    # Visualization
    fig = pygmt.Figure()
    # make color pallets
    pygmt.makecpt(
        cmap='etopo1',
        series='-8000/8000/1000',
        continuous=True
    )

    # plot high res topography
    fig.grdimage(
        grid=topo_data,
        region=[minlon, maxlon, minlat, maxlat],
        projection='M4i',
        shading=True,
        frame=True
    )

    # plot coastlines
    fig.coast(
        region=[minlon, maxlon, minlat, maxlat],
        projection='M4i',
        shorelines=True,
        frame=True
    )

    for idx, dff in enumerate(dfs):
        fig.plot(
            x=dff["Longitude"].values,
            y=dff["Latitude"].values,
            style="i10p",
            color=colorsList[idx],
            pen="black",
            label=networks[idx]
        )

    fig.legend(position="JTR+jTR+o0.2c", box=True)

    fig.savefig('station_map.png', crop=True, dpi=300)


if __name__ == '__main__':
    plot_stations()
