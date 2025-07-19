import matplotlib.pyplot as plt
import pickle

def plot_loss(loss_history, plot_path):
    plt.plot(loss_history["Train"], label="Train loss")
    plt.plot(loss_history["Val"], label="Val loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.grid()
    plt.legend()
    plt.savefig(plot_path+"/"+"loss.png")
    plt.close()

if __name__=="__main__":
    with open("./models/model_epoch_500_dv_bin"+"/"+"loss_history.pkl", "rb") as file:
        loss_history = pickle.load(file)
    plot_loss(loss_history, "./figures/model_epoch_500_dv_bin")
