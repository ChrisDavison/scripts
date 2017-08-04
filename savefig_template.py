FIGSAVE_CFG = {'project': 'project'
               , 'trial': 'trial'
               , 'task' : 'task'}

# Use `savefig(figure, *, project, trial, task, title=None, ext='png', **kwargs)`
# or simpler `savefig(figure, *, title=None, ext='png', **FIGSAVE_CFG, **kwargs)`
# to save a dated figure in a nested directory.
# -----------------------------------------------------------------------------
# Uses OS environment variable 'RESEARCHFIGURES' as parent directory
