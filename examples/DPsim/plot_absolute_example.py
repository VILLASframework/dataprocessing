from dataprocessing.plotdpsim import *

path = 'C:\\Users\\mmi\\git\\PowerSystemSimulation\\gre\\step-dist-init\\'
plot_dpsim_abs(path + 'lvector-ref.csv', 'reference', 2,
                    path + 'lvector0-local_rm-first-row.csv', 'local', 2)

plot_dpsim_abs(path + 'lvector-ref.csv', 'reference', 2,
                    path + 'lvector0-netem.csv', 'netem', 2)

plot_dpsim_abs(path + 'lvector-ref.csv', 'reference', 2,
                    path + 'lvector0-dist.csv', 'dist', 2)