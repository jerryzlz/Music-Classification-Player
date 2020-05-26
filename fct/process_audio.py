import librosa
import math
import mutagen
import os
import tempfile
from pydub import AudioSegment
from fct import file

data = {
    "mfcc": [],
    "filename": []
}


def split_audio(file_path, tmp_file_path, sample_rate=22050, duration=30):
    """
    对输入文件夹内的音频预处理
    :param file_path: 输入文件夹路径
    :param tmp_file_path: 临时文件夹路径
    :param sample_rate: 采样率
    :param duration: 预处理剪切时长
    :return:
    """
    filename = os.listdir(file_path)
    data["filename"].extend(filename)
    file.create_dir(tmp_file_path)
    duration = 30 + duration

    for i in range(len(filename)):
        if filename[i][-3:] == "mp3":
            song = AudioSegment.from_mp3(file_path + filename[i]).set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "ogg":
            song = AudioSegment.from_ogg(file_path + filename[i]).set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "wav":
            song = AudioSegment.from_wav(file_path + filename[i]).set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "wma":
            song = AudioSegment.from_file(file_path + filename[i], format="wma").set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "aac":
            song = AudioSegment.from_file(file_path + filename[i], format="aac").set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "m4a":
            song = AudioSegment.from_file(file_path + filename[i], format="m4a").set_frame_rate(sample_rate).set_channels(1)
        elif filename[i][-3:] == "lac":
            song = AudioSegment.from_file(file_path + filename[i], format="flac").set_frame_rate(sample_rate).set_channels(1)
        else:
            print("{}未知的/不支持的音乐格式".format(filename[i]))
            return

        split = song[30 * 1000: duration * 1000]
        fn = tmp_file_path + str(i) + ".wav"
        split.export(fn, format="wav")
        print("读取完成 {} / {}".format(i + 1, len(filename)))

    print("全部读取完成")


def get_mfcc(file_path, sample_rate=22050, duration=30, segments=10, n_mfcc=13, n_fft=2048, n_hop_length=512):
    """
    获取音频特征数据
    :param file_path: 临时文件夹路径
    :param sample_rate: 采样率
    :param duration: 预处理剪切时长
    :param segments: 切片数量
    :param n_mfcc: n维的音频特征
    :param n_fft: 短时傅里叶变换大小
    :param n_hop_length: 快速傅里叶变换步幅
    :return: data[mfcc, 文件名]
    """
    filename = os.listdir(file_path)
    samples_per_segment = int(sample_rate * duration / segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / n_hop_length)

    for f in filename:
        # load audio file
        abspath = os.path.join(file_path, f)
        sgn, sample_rate = librosa.load(abspath, sr=sample_rate)

        for d in range(segments):
            start = samples_per_segment * d
            finish = start + samples_per_segment

            mfcc = librosa.feature.mfcc(sgn[start:finish], sample_rate, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=n_hop_length)
            mfcc = mfcc.T
            if len(mfcc) == num_mfcc_vectors_per_segment:
                data["mfcc"].append(mfcc.tolist())
    print("mfcc获取完成")
    return data


def get_cover(file_name):
    """
    获取音频文件中的封面
    :param file_name: 文件名
    :return: 封面的临时文件路径
    """
    audio = mutagen.File(file_name)
    try:
        temp = tempfile.mktemp()
        open(temp, 'wb').write(audio.tags['APIC:'].data)
        return temp
    except:
        return "images/c.jpg"


def get_music_length(file_name):
    """
    获取音频文件的时长
    :param file_name: 文件名
    :return: 音频文件的时长（s）
    """
    audio = mutagen.File(file_name)
    return audio.info.length


def get_song_info(file_name):
    """
    获取音频文件id3信息
    :param file_name: 文件名
    :return: [song_name, artist, album]
    """
    audio = mutagen.File(file_name)
    song_name = audio.tags['TIT2']
    artist = audio.tags['TPE1']
    album = audio.tags['TALB']
    return song_name, artist, album

