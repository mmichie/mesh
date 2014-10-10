import os

mesh_dir = os.path.expanduser('~') + '/.mesh/'
db_filename = mesh_dir + 'history.sqlite'
no_fork_mode = False

if not os.path.exists(mesh_dir):
    os.makedirs(mesh_dir)
