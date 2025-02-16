from sim_utils4 import *

max_hidden_unit = 18

## Initial Sample Size
nN = 2000

X_mat, Y_true = generate_data(nN = nN)
sigma = 0.5
random_err = np.random.normal(loc = 0, scale = sigma, size = nN).reshape(Y_true.shape)
Y = Y_true + random_err

# data
data = {
    'x0':X_mat[0,:],
    'x1':X_mat[1,:],
    'y':Y
}


"""We now check the performance of the function fitting based on
1. Shallow ReLU neural network with number of hidden units as $\lfloor n^{1/3}\rfloor$.
2. Deep ReLU neural network with number of hidden layers as $\lfloor n^{1/3}\rfloor$ and each hidden layer contains 10 hidden units.
3. Deep ReLU neural network with $\lfloor n^{1/6}\rfloor$ hidden layers and each hidden layer contains $\lfloor n^{1/6}\rfloor$ hidden units.

##### Tag = 0
"""

gamma = 0.5
batches = 20
n_train = np.floor(nN * gamma).astype(int)
n_test  = nN - n_train

tag = 0
batch_size = np.minimum(np.floor(n_train/batches).astype(int), np.floor(n_test/batches).astype(int)).astype(int)
train_id = np.random.choice(nN, size = n_train, replace = False)
test_id = np.setdiff1d(range(nN), train_id)
X_tag = X_mat[tag,:].reshape((1, nN))
X_train  = X_tag[:,train_id]
Y_train = Y[:,train_id]
Y_test  = Y[:,test_id]

p_lm = get_linear_reg_p_val(X_tag.T, Y.T)
print(p_lm)

mse_test_nn = np.mean(np.power(Y_test - np.mean(Y_test), 2))

# Fit a shallow neural network
deg = 1/3
mult = 3/4
optimizer = 'sgd'
epochs_nn = 200
early_stopping = False
validation_split = 0.2
patience_nn = 20
min_delta = 0
drop_rate = 0.05
verbose = 0

n_h = np.floor(np.power(nN, deg)).astype(int)
mse_train_nn, predict_nn = fit_shallow_relu_nn(X_train, Y_train, n_h,
                                                optimizer = optimizer, epochs = epochs_nn,
                                                batch_size = batch_size,
                                                early_stopping = early_stopping,
                                                validation_split = validation_split,
                                                patience = patience_nn,
                                                min_delta = min_delta,
                                                drop_rate = drop_rate,
                                                verbose = verbose)

plus = False
kappa_nn = calculate_kappa(Y_train, predict_nn, plus = plus)
p_nn = get_dnn_p_val(mse_train_nn, mse_test_nn, n_train, n_test, kappa_nn)

mse_test_dnn = np.mean(np.power(Y_test - np.mean(Y_test), 2))

# fit a deep neural network of type 1
num_layers = np.floor(np.power(nN, deg)).astype(int)
num_nodes = np.repeat(max_hidden_unit, num_layers)
mse_train_dnn, predict_dnn = fit_deep_relu_nn(X_train, Y_train, num_nodes, num_layers,
                                              optimizer = optimizer, epochs = epochs_nn,
                                              batch_size = batch_size,
                                              early_stopping = early_stopping,
                                              validation_split = validation_split,
                                              patience = patience_nn,
                                              min_delta = min_delta,
                                              drop_rate = drop_rate,
                                              verbose = verbose)

kappa_dnn = calculate_kappa(Y_train, predict_dnn, plus = plus)
p_dnn = get_dnn_p_val(mse_train_dnn, mse_test_dnn, n_train, n_test, kappa_dnn)

mse_test_dnn2 = np.mean(np.power(Y_test - np.mean(Y_test), 2))

# fit a deep neural network of type 2
num_layers2 = np.floor(np.power(nN, mult*deg)).astype(int)
num_nodes2 = np.repeat(num_layers2, num_layers2)
mse_train_dnn2, predict_dnn2 = fit_deep_relu_nn(X_train, Y_train, num_nodes2, num_layers2,
                                                optimizer = optimizer, epochs = epochs_nn,
                                                batch_size = batch_size,
                                                early_stopping = early_stopping,
                                                validation_split = validation_split,
                                                patience = patience_nn,
                                                min_delta = min_delta,
                                                drop_rate = drop_rate,
                                                verbose = verbose)

kappa_dnn2 = calculate_kappa(Y_train, predict_dnn2, plus = plus)
p_dnn2 = get_dnn_p_val(mse_train_dnn2, mse_test_dnn2, n_train, n_test, kappa_dnn2)

result0 = [p_lm[1],p_nn, p_dnn, p_dnn2]
"""##### Tag = 1"""

tag = 1
X_tag = X_mat[tag,:].reshape((1, nN))
X_train  = X_tag[:,train_id]

p_lm = get_linear_reg_p_val(X_tag.T, Y.T)
print(p_lm)

# Fit a shallow neural network
n_h = np.floor(np.power(nN, deg)).astype(int)
mse_train_nn, predict_nn = fit_shallow_relu_nn(X_train, Y_train, n_h,
                                               optimizer = optimizer, epochs = epochs_nn,
                                               batch_size = batch_size,
                                               early_stopping = early_stopping,
                                               validation_split = validation_split,
                                               patience = patience_nn,
                                               min_delta = min_delta,
                                               drop_rate = drop_rate,
                                               verbose = verbose)

kappa_nn = calculate_kappa(Y_train, predict_nn, plus = plus)
p_nn = get_dnn_p_val(mse_train_nn, mse_test_nn, n_train, n_test, kappa_nn)

# fit a deep neural network of type 1
num_layers = np.floor(np.power(nN, deg)).astype(int)
num_nodes = np.repeat(max_hidden_unit, num_layers)
mse_train_dnn, predict_dnn = fit_deep_relu_nn(X_train, Y_train, num_nodes, num_layers,
                                              optimizer = optimizer, epochs = epochs_nn,
                                              batch_size = batch_size,
                                              early_stopping = early_stopping,
                                              validation_split = validation_split,
                                              patience = patience_nn,
                                              min_delta = min_delta,
                                              drop_rate = drop_rate,
                                              verbose = verbose)

kappa_dnn = calculate_kappa(Y_train, predict_dnn, plus = plus)
p_dnn = get_dnn_p_val(mse_train_dnn, mse_test_dnn, n_train, n_test, kappa_dnn)

# fit a deep neural network of type 2
num_layers2 = np.floor(np.power(nN, mult*deg)).astype(int)
num_nodes2 = np.repeat(num_layers2, num_layers2)
mse_train_dnn2, predict_dnn2 = fit_deep_relu_nn(X_train, Y_train, num_nodes2, num_layers2,
                                                optimizer = optimizer, epochs = epochs_nn,
                                                batch_size = batch_size,
                                                early_stopping = early_stopping,
                                                validation_split = validation_split,
                                                patience = patience_nn,
                                                min_delta = min_delta,
                                                drop_rate = drop_rate,
                                                verbose = verbose)

kappa_dnn2 = calculate_kappa(Y_train, predict_dnn2, plus = plus)
p_dnn2 = get_dnn_p_val(mse_train_dnn2, mse_test_dnn2, n_train, n_test, kappa_dnn2)

result1 = [p_lm[1],p_nn, p_dnn, p_dnn2]