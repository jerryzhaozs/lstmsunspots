import numpy as np
import random
#定义神经网络
class Network(object):
    def __init__(self,sizes):
        self.sizes=sizes
        self.num_layers=len(sizes)
        self.biases=[np.random.randn(y,1) for y in sizes[1:]]
        self.weights=[np.random.randn(y,x) for x,y in zip(sizes[:-1],sizes[1:])]
        self.acclist=[]
# Press the green button in the gutter to run the script.
    def feedforward(self,x):
        for b,w in zip(self.biases,self.weights):
            x=sigmoid(np.dot(w,x)+b)
        return x

    def backprop(self,x,y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        zs=[]
        activation=x
        activations=[x]
        for b,w in zip(self.biases,self.weights):
            z=np.dot(w,activation)+b
            zs.append(z)
            activation=sigmoid(z)
            activations.append(activation)
        #反向更新
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_layers):
            sp= sigmoid_prime(zs[-l])
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return nabla_b, nabla_w

    def cost_derivative(self,output_activations,y):
        return output_activations-y

    def GD(self,training_data,epochs,eta,test_data):
        for j in range(epochs):
            random.shuffle(training_data)
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            for x, y in training_data:
                delta_nabla_b, delta_nabla_w = self.backprop(x, y)
                nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
                nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            self.biases = [b - (eta/len(training_data) * nb) for b, nb in zip(self.biases, nabla_b)]
            self.weights = [w - (eta/len(training_data) * nw) for w, nw in zip(self.weights, nabla_w)]
            print(f"epoch{j}" )

    def update_mini_batch(self,mini_batch,eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.biases = [b - (eta/len(mini_batch) * nb) for b, nb in zip(self.biases, nabla_b)]
        self.weights = [w - (eta/len(mini_batch) * nw) for w, nw in zip(self.weights, nabla_w)]

    def SGD(self,training_data,epochs,eta,mini_batch_size,test_data=None):
        if test_data:
            n_test=len(list(test_data))
        n=len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches=[training_data[k:k+mini_batch_size] for k in range(0,n,mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch,eta)
            if test_data:
                print(f"epoch{j}:{self.evaluate(test_data)}/{n_test} complete")
                self.acclist.append(self.evaluate(test_data)/n_test)
            print(f"epoch{j} complete")

    def evaluate(self,test_data):
        test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

def sigmoid(z):
    return 1.0/(1+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

if __name__ == '__main__':
    import mnist_loader
    data=[(np.array([[0.2],[0.6],[0.1]]),np.array([[0],[1.0]])),(np.array([[0.2],[0.3],[0.5]]),np.array([[0.1],[0.9]])),
            (np.array([[0.7],[0.2],[0.1]]),np.array([[0.25],[0.75]])),(np.array([[0.2],[0.3],[0.5]]),np.array([[0.15],[0.85]]))]
    t_data = [(np.array([0.2, 0.65, 0.15]), np.array([[0.35],[0.65]]))]
    net = Network([784, 30, 10])
    # net=Network([3,2,2])
    # print(net.weights)
    #y=net.feedforward(np.array([[0.02],[0.25],[0.01]]))
    # print(y)
    # print(mean_squared_error(y,np.array([[0.25],[0.75]])))
    training_data, validation_data, test_data= mnist_loader.load_data_wrapper()
    training_data=list(training_data)
    test_data=list(test_data)
    #print(net.evaluate(test_data))
    #print(training_data[0])
    net.SGD(training_data,3,3,100,test_data=test_data)
    # for x,y in data:
    #      print(net.backprop(x,y))
    import matplotlib.pyplot as plt
    plt.plot(range(3), net.acclist, 'o-', label="Test_Accuracy")
    plt.xlabel('Epochs')
    plt.ylabel('Test accuracy')
    plt.title('Test accuracy vs. epoches')
    plt.show()