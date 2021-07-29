import h5py


f = h5py.File('complete_data_xception_model.h5', 'r')
list(f.keys())