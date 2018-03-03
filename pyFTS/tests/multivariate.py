import pandas as pd
import matplotlib.pylab as plt
from pyFTS.data import TAIEX as tx
from pyFTS.common import Transformations


from pyFTS.data import SONDA
df = SONDA.get_dataframe()
train = df.iloc[0:1572480] #three years
test = df.iloc[1572480:2096640] #ears
del df

from pyFTS.partitioners import Grid, Util as pUtil
from pyFTS.common import Transformations
from pyFTS.models.multivariate import common, variable, mvfts
from pyFTS.models.seasonal import partitioner as seasonal
from pyFTS.models.seasonal.common import DateTime

bc = Transformations.BoxCox(0)
diff = Transformations.Differential(1)

np = 10

model = mvfts.MVFTS("")

fig, axes = plt.subplots(nrows=5, ncols=1,figsize=[15,10])

sp = {'seasonality': DateTime.day_of_year , 'names': ['Jan','Feb','Mar','Apr','May','Jun','Jul', 'Aug','Sep','Oct','Nov','Dec']}

vmonth = variable.Variable("Month", data_label="datahora", partitioner=seasonal.TimeGridPartitioner, npart=12,
                           data=train, partitioner_specific=sp)
model.append_variable(vmonth)

sp = {'seasonality': DateTime.minute_of_day}

vhour = variable.Variable("Hour", data_label="datahora", partitioner=seasonal.TimeGridPartitioner, npart=24,
                          data=train, partitioner_specific=sp)
model.append_variable(vhour)

vhumid = variable.Variable("Humidity", data_label="humid", partitioner=Grid.GridPartitioner, npart=np, data=train)
model.append_variable(vhumid)

vpress = variable.Variable("AtmPress", data_label="press", partitioner=Grid.GridPartitioner, npart=np, data=train)
model.append_variable(vpress)

vrain = variable.Variable("Rain", data_label="rain", partitioner=Grid.GridPartitioner, npart=20, data=train)#train)
model.append_variable(vrain)

model.target_variable = vrain

model.fit(train, num_batches=20, save=True, batch_save=True, file_path='mvfts_sonda3', distributed=True,
          nodes=['192.168.0.110','192.168.0.106'])
