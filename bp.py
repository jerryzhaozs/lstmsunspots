import numpy as np
import random

class Network(object):
    def __init__(self, sizes):  # sizes  [3,2,2]
        # 网络层数
        self.num_layers = len(sizes)
        # 每层神经元个数
        self.sizes = sizes
        # 初始化每层偏置和权重
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)/np.sqrt(x) for x, y in zip(sizes[:-1], sizes[1:])]
        # self.weights=[]
        # for x,y in zip(sizes[:-1],sizes[1:]):
        #     self.weights.append(np.random.randn(x,y))
        self.acc_list=[] #精度列表
        self.loss_list=[]
    def feedforward(self, x):  # x是3行1列的输入
        for w, b in zip(self.weights, self.biases):
            x = sigmoid(np.dot(w, x) + b)
        return x

    def cost_derivative(self, output_activation, y):
        return output_activation - y

    # 反向传播求每层偏导
    def backprop(self, x, y):
        # 保存每一层偏导，初始化为全0
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        zs = []
        activation = x
        activations = [x]
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # 反向更新
        # 从最后一层开始，反着更新每一层的w,b
        # 最后一层
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        # 最后一层权重和偏执的导数
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # 从倒数第二层到输入层
        for l in range(2, self.num_layers):
            sp = sigmoid_prime(zs[-l])
            # 计算当前层的误差
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            # 保存当前层的偏置和权重的导数
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return nabla_b,nabla_w
    def SGD(self,training_data,mini_batch_size,epochs,eta,test_data=None):
        """
        随机梯度下降算法
        :param training_data:训练数据
        :param epochs: 迭代次数
        :param eta :学习率
        :param  test_data :测试集
        """
        if test_data: #测试集如果存在
            n_test=len(test_data)
        #开始训练每一个epochs
        for j in range(epochs):
            # 保存每一层偏导，初始化为0
            random.shuffle(training_data)  #顺序打乱
            #训练样本总数
            n = len(training_data)
            #按小样本数量划分训练集
            mini_batches=[training_data[k:k+mini_batch_size] for k in range(0,n,mini_batch_size)]
            for mini_batch in mini_batches:
                # 对每个样本求偏导并保存
                self.update_mini_batch(mini_batch,eta)
            if test_data:
                acc=self.evaluate(test_data) #计算测试集精度
                self.acc_list.append(acc/n_test) #将精度追加至列表
                test_loss=self.mean_square_loss(test_data)
                self.loss_list.append(test_loss)
                print(f"Epoch{j}:{acc}/{n_test} ,test_loss:{test_loss}") #在测试集的准确率
            print(f"Epoch{j} complete")
    def evaluate(self,test_data): #计算正确识别的总量
        test_results=[]
        for x,y in test_data:
            y_hat=np.argmax(self.feedforward(x))
            test_results.append((y_hat,y))
        return sum((int(y_hat==y))for y_hat,y in test_results)
    def update_mini_batch(self,mini_batch,eta):
        #根据biases和weights的行列创建对应的全部元素值为0的矩阵
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x,y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            # 累加所有样本w,b的和
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            # 更新权重和偏执
        self.biases = [b - (eta/len(mini_batch) * nb) for b, nb in zip(self.biases, nabla_b)]
        self.weights = [w - (eta/len(mini_batch) * nw) for w, nw in zip(self.weights, nabla_w)]
    def mean_square_loss(self,data):
        #均方查损失函数计算误差
        loss=0
        for x,y in data:
            y_hat=self.feedforward(x)
            if y.ndim==0: #如果是测试集
                t=np.zeros([10,1])
                t[y]=1
                y=t
            loss+=np.sum(np.square(y_hat-y))*0.5
        return loss/len(data)

# sigmoid函数
def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))

# sigmoid函数偏导
def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))

if __name__ == '__main__':
    import mnist_loader
    training_data,validation_data,test_data=mnist_loader.load_data_wrapper()
    training_data=list(training_data)
    test_data=list(test_data)
    net=Network([784,50,10])
    net.SGD(training_data,100,3,0.01,test_data)

    # 画测试集的精度图
    import matplotlib.pyplot as plt

    plt.plot(range(5), net.acc_list, 'o-')

    plt.plot(range(5), net.loss_list, 'o-')
    plt.show()



# %%
