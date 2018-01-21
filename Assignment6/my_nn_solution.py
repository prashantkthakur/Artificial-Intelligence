import numpy as np
import neuralnetworks as nn
import mlutils as ml
import time


def trainNNs(X, T, trainFraction, hiddenLayerStructures, numberRepetitions, numberIterations, classify):
    results = []

    # Do tasks here
    for h_layer in hiddenLayerStructures:
        start = time.time()
        train_rmse = []
        test_rmse = []
        for repetition in range(numberRepetitions):
            Xtrain, Ttrain, Xtest, Ttest = ml.partition(X, T, (trainFraction, 1 - trainFraction),
                                                        classification=classify)
            if classify:
                nnet = nn.NeuralNetworkClassifier(X.shape[1], h_layer, T.shape[1])
                nnet.train(Xtrain, Ttrain, numberIterations)
                predTest, probsTest, _ = nnet.use(Xtest, allOutputs=True)  # discard hidden unit outputs
                ml.percentCorrect(predTest, Ttest)


            else:
                nnet = nn.NeuralNetwork(X.shape[1], h_layer, T.shape[1])
                nnet.train(Xtrain, Ttrain, numberIterations)
                Ytrain = nnet.use(Xtrain)
                Ytest = nnet.use(Xtest)
                trn_rmse = np.sqrt(np.mean((Ytrain - Ttrain) ** 2))
                tst_rmse = np.sqrt(np.mean((Ytest - Ttest) ** 2))
                train_rmse.append(trn_rmse)
                test_rmse.append(tst_rmse)

            if repetition == (numberRepetitions - 1):
                total_time = time.time() - start
                results.append([h_layer, train_rmse, test_rmse, total_time])

    # End tasks

    # print(results)
    return results


def summary(results):
    output = []
    for val in results:
        output.append([val[0], np.mean(val[1]), np.mean(val[2]), val[-1]])
    return output


def bestNetwork(summaries):
    val = np.array(summaries, dtype=object)
    idx = np.argmin(val[:, 2])
    return summaries[idx]


X = np.arange(10).reshape((-1, 1))
T = X + 1 + np.random.uniform(-1, 1, ((10, 1)))
X.shape, T.shape
nnet = nn.NeuralNetwork(X.shape[1], 2, T.shape[1])
nnet.train(X, T, 5)
# print(nnet.getErrorTrace())
# result = trainNNs(X, T, 0.8, [0, 10, [10, 10]], 5, 100, classify=False)
# result = trainNNs(X, T, 0.8, [0, 1, 2, 10, [10, 10], [5, 5, 5, 5], [2]*5], 50, 400, classify=False)
# print(result[0])
# print(bestNetwork(summary(result)))
print(bestNetwork(([[[1, 1], 1.3, 2.3, 0.5], [[2, 2, 2], 4.3, 1.3, 0.6]])))
