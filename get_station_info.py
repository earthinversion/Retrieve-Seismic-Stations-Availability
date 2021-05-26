from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import sys
from plot_stations import plot_stations

from obspy.clients.fdsn.header import URL_MAPPINGS
# for key in sorted(URL_MAPPINGS.keys()):
#     print("{0:<11} {1}".format(key,  URL_MAPPINGS[key]))
all_clients = list(URL_MAPPINGS.keys())
all_clients.remove('IRIS')
all_clients = ['IRIS'] + all_clients
# print(all_clients)

# Define parameters
starttime = UTCDateTime("2020-05-15T00:00:00Z")
endtime = starttime+7*24*3600
net = "NC"
stn = "*"
channel = "*Z"
count = 0
success = False
for cl in all_clients:
    try:
        print(f"--> Trying for client: {cl}")
        client = Client(cl)

        inventory = client.get_stations(network=net, station=stn, channel=channel,
                                        level="response", starttime=starttime, endtime=endtime)

        print(inventory)

        inventory.write('station_info.txt', 'STATIONTXT', level='station')
        success = True
        if success:
            try:
                plot_stations()
            except:
                sys.exit()
            break
    except KeyboardInterrupt:
        sys.exit()
    except:
        print(cl, sys.exc_info())
    count += 1
