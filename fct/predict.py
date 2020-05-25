import numpy as np
import tensorflow.keras as keras


def predict(algorithm, data, genres):
    """
    选择模型并进行预测
    :param algorithm: 选择模型
    :param data:
    :param genres:
    :return: info[文件名, 分类结果, 段落分类结果]
    """

    if algorithm == "CNN":
        model = keras.models.load_model("model\\CNN.h5")
    else:
        return

    feature = np.array(data["mfcc"])
    feature = feature[..., np.newaxis]
    try:
        predict = model.predict(feature)
    except:
        print("文件夹为空")
        return
    predict_index = list(np.argmax(predict, axis=1))
    predict_list, predict_result = [], []
    length = int(len(predict_index) / 10)

    for i in range(length):
        start = int(str(i) + "0")
        end = int(str(i+1) + "0")
        predict_list.append(predict_index[start:end])
    for i in range(len(predict_list)):
        counts = np.bincount(predict_list[i])
        predict_result.append(genres[np.argmax(counts)])

    info = data["filename"], predict_result, predict_list
    print("分类完成")
    return info
