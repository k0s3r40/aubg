import json
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from be_client import SomethingWayClient
from prep_data import DataArrange





creds = {"email": "kostadin@slavov.net",
         "password": "verysecure",
         }
cli = SomethingWayClient()

cli.login(creds)

fig, (HUM, AQ, TEMP) = plt.subplots(3, 1)
fig.suptitle('Aura')

resp = cli.fetch()
data = DataArrange(resp)
data.get_data()

# Some example data to display


HUM.plot(data.HUM.keys(), data.HUM.values(), '.-')
HUM.set_ylabel('Humidity')
HUM.yaxis.set_major_locator(plt.MaxNLocator(10))

AQ.plot(data.GR.keys(), data.GR.values(), '.-')
AQ.set_ylabel('Air quality')
AQ.yaxis.set_major_locator(plt.MaxNLocator(10))

TEMP.plot(data.TMP.keys(), data.TMP.values(), '.-')
TEMP.set_ylabel('Temp')
TEMP.yaxis.set_major_locator(plt.MaxNLocator(10))
plt.ion()
plt.locator_params(axis='y', nbins=6)
while True:
    resp = cli.fetch()
    data = DataArrange(resp)
    data.get_data()

    # Some example data to display

    HUM.plot(data.HUM.keys(), data.HUM.values(), '.-')

    AQ.plot(data.GR.keys(), data.GR.values(), '.-')

    TEMP.plot(data.TMP.keys(), data.TMP.values(), '.-')
    y = np.random.random([10, 1])

    plt.show()
    plt.pause(0.0001)



    # axs[0].plot(data.HUM.keys(), data.HUM.values())
    # plt.show()
    sleep(1)
    # break



# with open('response.json', 'w') as f:
#     f.write(json.dumps(resp))

