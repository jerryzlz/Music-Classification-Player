import os
import pygame
import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from fct import process_audio, predict, file


class Index(QtWidgets.QWidget):
    def __init__(self, dir_path, settings):
        """
        初始化GUI
        :param dir_path: 主程序所在目录
        :param settings:  设置参数
        """
        super(Index, self).__init__()
        self.dir_path = dir_path
        self.settings = settings
        self.status = -1

        pygame.mixer.init()

        self.setStyleSheet("background-color:#1c2529;")
        self.setWindowTitle("音乐分类播放器")
        self.setGeometry(5, 10, 1280, 720)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.center()

        self.setWindowIcon(QtGui.QIcon("images\\logo.ico"))

        self.left_win = QtWidgets.QLabel(self)
        self.left_win.setStyleSheet("background-color:#02e494;")
        self.left_win.setGeometry(0, 0, 350, 720)

        self.bottom_win = QtWidgets.QLabel(self)
        self.bottom_win.setStyleSheet("background-color:#fff;")
        self.bottom_win.setGeometry(0, 640, 1280, 80)

        self.btn_min = QtWidgets.QPushButton(self)
        self.btn_min.setStyleSheet('background-color:#00ff00;border-radius:5px;')
        self.btn_min.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_min.setGeometry(0, 0, 23, 23)
        self.btn_min.setText("")
        self.btn_min.move(1160, 60)

        self.btn_close = QtWidgets.QPushButton(self)
        self.btn_close.setStyleSheet('background-color:#ff0000;border-radius:5px;')
        self.btn_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close.setGeometry(0, 0, 23, 23)
        self.btn_close.setText("")
        self.btn_close.move(1200, 60)

        self.logo = QtWidgets.QPushButton(self.left_win)
        self.logo.setStyleSheet("border:None;")
        self.logo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.logo.setIcon(QtGui.QIcon("images\\Sangeetic_s.png"))
        self.logo.setIconSize(QtCore.QSize(139, 60))
        self.logo.move(100, 20)

        self.cover = QtWidgets.QLabel(self.left_win)
        self.cover.setStyleSheet("border-radius:5px;")
        self.cover.setScaledContents(True)
        self.cover.setPixmap(QtGui.QPixmap("images/c.jpg"))
        self.cover.setGeometry(55, 370, 240, 240)

        self.left_list = QtWidgets.QListWidget(self.left_win)
        self.left_list.setStyleSheet("font-size:30px;color:#fff;font-family:微软雅黑;border:None;")
        self.left_list.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left_list.insertItem(0, '主页')
        self.left_list.insertItem(1, '音乐分类')
        self.left_list.insertItem(2, '已分类的音乐')
        self.left_list.insertItem(3, "设置")

        self.left_list.setSpacing(10)
        self.left_list.setGeometry(55, 95, 230, 240)
        self.left_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.stack1 = QtWidgets.QWidget()
        self.stack2 = QtWidgets.QWidget()
        self.stack3 = QtWidgets.QWidget()
        self.stack4 = QtWidgets.QWidget()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
        self.Stack.setGeometry(380, 110, 870, 510)

        self.process = QtWidgets.QProgressBar(self.bottom_win)
        self.process.setTextVisible(False)
        self.process.setStyleSheet("QProgressBar::chunk {background-color:#00ce85;""border-radius:5px;}")
        self.process.setOrientation(QtCore.Qt.Horizontal)
        self.process.setMinimum(0)
        self.process.setGeometry(0, 0, 1280, 5)

        self.song_name = QtWidgets.QLabel(self.bottom_win)
        self.song_name.setText("当前无音乐播放")
        self.song_name.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:23px;")
        self.song_name.setGeometry(20, 6, 470, 40)

        self.art_abl = QtWidgets.QLabel(self.bottom_win)
        self.art_abl.setText("艺人-专辑")
        self.art_abl.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:18px;")
        self.art_abl.setGeometry(20, 40, 470, 40)

        self.pp = QtWidgets.QPushButton(self.bottom_win)
        self.pp.setStyleSheet("border-radius:25px;border:None;")
        self.pp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pp.setIcon(QtGui.QIcon("images\\play.png"))
        self.pp.setIconSize(QtCore.QSize(50, 50))
        self.pp.setGeometry(570, 13, 50, 50)
        self.pp.setShortcut("Space")

        self.previous = QtWidgets.QPushButton(self.bottom_win)
        self.previous.setStyleSheet("border-radius:20px;border:None;")
        self.previous.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.previous.setIcon(QtGui.QIcon("images\\previous.png"))
        self.previous.setIconSize(QtCore.QSize(40, 40))
        self.previous.setGeometry(510, 18, 40, 40)

        self.next = QtWidgets.QPushButton(self.bottom_win)
        self.next.setStyleSheet("border-radius:20px;border:None;")
        self.next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next.setIcon(QtGui.QIcon("images\\next.png"))
        self.next.setIconSize(QtCore.QSize(40, 40))
        self.next.setGeometry(640, 18, 40, 40)

        self.play_time_s = QtWidgets.QLabel(self.bottom_win)
        self.play_time_s.setNum(0)
        self.play_time_s.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:23px;")
        self.play_time_s.setGeometry(915, 25, 30, 30)

        self.split = QtWidgets.QLabel(self.bottom_win)
        self.split.setText(":")
        self.split.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:23px;")
        self.split.setGeometry(895, 25, 10, 30)

        self.play_time_t = QtWidgets.QLabel(self.bottom_win)
        self.play_time_t.setNum(0)
        self.play_time_t.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:23px;")
        self.play_time_t.setGeometry(865, 25, 30, 30)

        self.circle = QtWidgets.QPushButton(self.bottom_win)
        self.circle.setStyleSheet("border:None;")
        self.circle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if settings["loop"] == "1":
            self.circle.setIcon(QtGui.QIcon("images\\loop_1.png"))
        elif settings["loop"] == "0":
            self.circle.setIcon(QtGui.QIcon("images\\loop.png"))
        self.circle.setIconSize(QtCore.QSize(30, 30))
        self.circle.setGeometry(970, 24, 30, 30)

        self.now_playing = QtWidgets.QLabel(self.bottom_win)
        self.now_playing.setText("正在播放")
        self.now_playing.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:23px;")
        self.now_playing.setGeometry(1030, 6, 480, 40)

        self.now_genres = QtWidgets.QLabel(self.bottom_win)
        self.now_genres.setText("未播放音乐")
        self.now_genres.setStyleSheet("color:#02e494;font-family:微软雅黑;font-size:18px;")
        self.now_genres.setGeometry(1030, 40, 400, 40)

        self.second = 0
        self.minute = 0

        self.volume = QtWidgets.QLabel(self.bottom_win)
        self.volume.setPixmap(QtGui.QPixmap("images\\volume.png"))
        self.volume.setScaledContents(True)
        self.volume.setGeometry(715, 30, 20, 20)

        self.volume_c = QtWidgets.QSlider(self.bottom_win)
        self.volume_c.setOrientation(QtCore.Qt.Horizontal)
        self.volume_c.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.volume_c.setMaximum(100)
        self.volume_c.setValue(50)
        self.volume_c.setSliderPosition(50)
        self.volume_c.setGeometry(745, 35, 80, 10)

        self.volume_c.valueChanged.connect(lambda: self.change_volume(self.volume_c.value()))
        self.left_list.currentRowChanged.connect(self.display)
        self.logo.clicked.connect(self.open_github)
        self.pp.clicked.connect(self.pp_c)
        self.previous.clicked.connect(self.previous_song)
        self.next.clicked.connect(self.next_song)
        self.circle.clicked.connect(self.loop)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_close.clicked.connect(self.close)

    def stack1UI(self):
        """
        主页
        :return:
        """
        layout = QtWidgets.QVBoxLayout()
        line = QtWidgets.QLabel()
        line.setText("开始探索音乐")
        line.setStyleSheet("font-size:55px;color:#fff;font-family:微软雅黑;")
        line1 = QtWidgets.QLabel()
        line1.setStyleSheet("font-size:52px;color:#02e494;font-family:微软雅黑;")
        line1.setText("HIPHOP  金属  POP  乡村  PUNK")
        line2 = QtWidgets.QLabel()
        line2.setStyleSheet("font-size:45px;color:#08a872;font-family:微软雅黑;")
        line2.setText("摇滚  DISCO  流行  BLUES  古典  REGGAE")
        line3 = QtWidgets.QLabel()
        line3.setStyleSheet("font-size:40px;color:#128c66;font-family:微软雅黑;")
        line3.setText("COUNTRY  布鲁斯  JAZZ  朋克  ROCK  爵士")
        line4 = QtWidgets.QLabel()
        line4.setStyleSheet("font-size:35px;color:#107052;font-family:微软雅黑;")
        line4.setText("嘻哈  CLASSICAL  爵士  METAL  金属  POP  流行  JAZZ")
        line5 = QtWidgets.QLabel()
        line5.setStyleSheet("font-size:30px;color:#234e47;font-family:微软雅黑;")
        line5.setText("BLUES  古典  POP  迪斯科  HIPHOP  摇滚  PUNK  雷鬼  DISCO")
        layout.addWidget(line)
        layout.addWidget(line1)
        layout.addWidget(line2)
        layout.addWidget(line3)
        layout.addWidget(line4)
        layout.addWidget(line5)
        self.stack1.setLayout(layout)

    def stack2UI(self):
        """
        音乐分类页
        :return:
        """
        layout = QtWidgets.QVBoxLayout()
        line = QtWidgets.QLabel()
        line.setText("开始音乐分类")
        line.setStyleSheet("font-size:55px;color:#fff;font-family:微软雅黑;")
        line1 = QtWidgets.QLabel()
        line1.setText('请确保要分类的文件已放在本程序目录下的"input"文件夹下！')
        line1.setStyleSheet("font-size:30px;color:#fff;font-family:微软雅黑;")
        file_box = QtWidgets.QFileSystemModel()
        file_box.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        file_box.setRootPath(file.dir_name(self.dir_path)[1])
        model = QtGui.QStandardItemModel()
        treeview = QtWidgets.QTreeView()
        treeview.setModel(model)
        treeview.setWindowTitle("input文件夹")
        treeview.setStyleSheet("color:#fff;font-size:20px;")
        file_name = []
        path_dataname = model.invisibleRootItem()
        all_file = os.listdir(file.dir_name(self.dir_path)[1])
        all_file.sort()
        for j in range(len(all_file)):
            if not os.path.isdir(self.dir_path + '\\' + all_file[j]):
                file_name.append(all_file[j])
        for i in range(len(file_name)):
            data = QtGui.QStandardItem(file_name[i])
            path_dataname.setChild(i, data)
        self.submit = QtWidgets.QPushButton()
        self.submit.setText("开始分类")
        self.submit.setStyleSheet("color:#fff;font-size:28px;font-family:微软雅黑;")
        self.submit.clicked.connect(self.run_cls)
        layout.addWidget(line)
        layout.addWidget(line1)
        layout.addWidget(treeview)
        layout.addWidget(self.submit)
        self.stack2.setLayout(layout)

    def stack3UI(self):
        """
        已分类的音乐页
        :return:
        """
        layout = QtWidgets.QVBoxLayout()
        layout1 = QtWidgets.QHBoxLayout()
        layout2 = QtWidgets.QHBoxLayout()
        layout3 = QtWidgets.QHBoxLayout()
        line = QtWidgets.QLabel()
        blues = QtWidgets.QPushButton()
        classical = QtWidgets.QPushButton()
        country = QtWidgets.QPushButton()
        disco = QtWidgets.QPushButton()
        hiphop = QtWidgets.QPushButton()
        jazz = QtWidgets.QPushButton()
        metal = QtWidgets.QPushButton()
        pop = QtWidgets.QPushButton()
        reggae = QtWidgets.QPushButton()
        rock = QtWidgets.QPushButton()

        blues.setText("布鲁斯 / Blues")
        blues.setStyleSheet("background-color:#3f51b5;color:#fff;font-size:25px;font-family:微软雅黑;")
        blues.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        classical.setText("古典 / Classical")
        classical.setStyleSheet("background-color:#263238;color:#fff;font-size:25px;font-family:微软雅黑;")
        classical.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        country.setText("乡村 / Country")
        country.setStyleSheet("background-color:#ff9800;color:#fff;font-size:25px;font-family:微软雅黑;")
        country.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        disco.setText("迪斯科 / Disco")
        disco.setStyleSheet("background-color:#4527a0;color:#fff;font-size:25px;font-family:微软雅黑;")
        disco.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        hiphop.setText("嘻哈 / Hiphop")
        hiphop.setStyleSheet("background-color:#616161;color:#fff;font-size:25px;font-family:微软雅黑;")
        hiphop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        jazz.setText("爵士 / Jazz")
        jazz.setStyleSheet("background-color:#01579b;color:#fff;font-size:25px;font-family:微软雅黑;")
        jazz.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        metal.setText("金属 / Metal")
        metal.setStyleSheet("background-color:#b71c1c;color:#fff;font-size:25px;font-family:微软雅黑;")
        metal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        pop.setText("流行 / Pop")
        pop.setStyleSheet("background-color:#66bb6a;color:#fff;font-size:25px;font-family:微软雅黑;")
        pop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        reggae.setText("雷鬼 / Reggae")
        reggae.setStyleSheet("background-color:#ffc107;color:#fff;font-size:25px;font-family:微软雅黑;")
        reggae.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        rock.setText("摇滚 / Rock")
        rock.setStyleSheet("background-color:#e53935;color:#fff;font-size:25px;font-family:微软雅黑;")
        rock.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        blues.clicked.connect(lambda: (self.play("blues")))
        classical.clicked.connect(lambda: self.play("classical"))
        country.clicked.connect(lambda: self.play("country"))
        disco.clicked.connect(lambda: self.play("disco"))
        hiphop.clicked.connect(lambda: self.play("hiphop"))
        jazz.clicked.connect(lambda: self.play("jazz"))
        metal.clicked.connect(lambda: self.play("metal"))
        pop.clicked.connect(lambda: self.play("pop"))
        reggae.clicked.connect(lambda: self.play("reggae"))
        rock.clicked.connect(lambda: self.play("rock"))
        line.setText("已分类的音乐")
        line.setStyleSheet("font-size:55px;color:#fff;font-family:微软雅黑;")

        self.file_box = QtWidgets.QListWidget()
        self.file_box.setStyleSheet("color:#fff;font-size:20px;")

        layout1.addWidget(blues)
        layout1.addWidget(classical)
        layout1.addWidget(country)
        layout1.addWidget(disco)
        layout2.addWidget(hiphop)
        layout2.addWidget(jazz)
        layout2.addWidget(metal)
        layout3.addWidget(pop)
        layout3.addWidget(reggae)
        layout3.addWidget(rock)
        layout.addWidget(line)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addWidget(self.file_box)
        self.stack3.setLayout(layout)

    def stack4UI(self):
        """
        设置页
        :return:
        """
        layout = QtWidgets.QVBoxLayout()
        line = QtWidgets.QLabel()
        line.setText("设置")
        line.setStyleSheet("font-size:55px;color:#fff;font-family:微软雅黑;")
        line1 = QtWidgets.QLabel()
        line1.setText("若不清楚用法请勿更改")
        line1.setStyleSheet("font-size:30px;color:#fff;font-family:微软雅黑;")
        form = QtWidgets.QFormLayout()
        self.sample_rate = QtWidgets.QLineEdit(str(self.settings["process_settings"]["sample_rate"]))
        self.sample_rate.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        sample_rate_text = QtWidgets.QLabel()
        sample_rate_text.setText("预处理采样率 （sample rate）")
        sample_rate_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        self.duration = QtWidgets.QLineEdit(str(self.settings["process_settings"]["duration"]))
        self.duration.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        duration_text = QtWidgets.QLabel()
        duration_text.setText("预处理剪切时长 （duration）")
        duration_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        self.segments = QtWidgets.QLineEdit(str(self.settings["process_settings"]["segments"]))
        self.segments.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        segments_text = QtWidgets.QLabel()
        segments_text.setText("预处理切片数量 （segments）")
        segments_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        self.mfcc = QtWidgets.QLineEdit(str(self.settings["process_settings"]["mfcc"]))
        self.mfcc.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        mfcc_text = QtWidgets.QLabel()
        mfcc_text.setText("预处理音频特征维度 （mfcc）")
        mfcc_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        self.fft = QtWidgets.QLineEdit(str(self.settings["process_settings"]["fft"]))
        self.fft.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        fft_text = QtWidgets.QLabel()
        fft_text.setText("快速傅里叶变换大小 （fft）")
        fft_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        self.hop_length = QtWidgets.QLineEdit(str(self.settings["process_settings"]["hop_length"]))
        self.hop_length.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")
        hop_length_text = QtWidgets.QLabel()
        hop_length_text.setText("快速傅里叶变换步幅 （hop length）")
        hop_length_text.setStyleSheet("color:#fff;font-size:25px;font-family:微软雅黑;")

        form.setSpacing(15)
        form.addRow(sample_rate_text, self.sample_rate)
        form.addRow(duration_text, self.duration)
        form.addRow(segments_text, self.segments)
        form.addRow(mfcc_text, self.mfcc)
        form.addRow(fft_text, self.fft)
        form.addRow(hop_length_text, self.hop_length)

        self.submit_settings = QtWidgets.QPushButton()
        self.submit_settings.setText("确定")
        self.submit_settings.setStyleSheet("color:#fff;font-size:28px;font-family:微软雅黑;")
        self.submit_settings.clicked.connect(self.change_settings)

        layout.addWidget(line)
        layout.addWidget(line1)
        layout.addLayout(form)
        layout.addWidget(self.submit_settings)
        self.stack4.setLayout(layout)

    def display(self, i):
        """
        切换页面
        :param i: 堆叠页面ID
        :return:
        """
        self.Stack.setCurrentIndex(i)

    def center(self):
        """
        将页面显示在屏幕中间
        :return:
        """
        pre_move = self.frameGeometry()
        mov = QtWidgets.QDesktopWidget().availableGeometry().center()
        pre_move.moveCenter(mov)
        self.move(pre_move.topLeft())

    @staticmethod
    def open_github(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/jerryzlz/Music-Classification-Player"))

    def timerEvent(self, event):
        """
        计时器
        :param event:
        :return:
        """
        self.second += 1
        if self.second == 60:
            self.minute += 1
            self.second = 0
        self.play_time_s.setNum(self.second)
        self.play_time_t.setNum(self.minute)

        self.time = self.second + self.minute * 60
        print(self.time)
        self.process.setValue(self.time)

        if self.timer == round(self.music_length):
            self.timer.stop()
        if not pygame.mixer.music.get_busy():
            self.next_song()

    def result_list(self, genres):
        """
        已分类的音乐列表
        :param genres: 音乐类型
        :return:
        """
        self.file_box.clear()
        for i in range(len(self.filename)):
            self.file_box.insertItem(i, self.filename[i])
        if pygame.mixer.music.get_busy():
            print(pygame.mixer.music.get_busy())

    def play(self, genres):
        """
        播放音乐槽函数
        :param genres: 音乐类型
        :return:
        """
        file.create_dir(file.dir_name(self.dir_path)[2])
        file.create_dir(file.dir_name(self.dir_path)[2] + str(genres) + "\\")
        self.play_file_path = str(self.dir_path) + "result\\" + str(genres) + "\\"
        self.filename = os.listdir(self.play_file_path)
        self.count = 0
        self.play_time_s.setNum(0)
        if self.filename:
            self.play_name = self.filename[self.count]
            pygame.mixer.music.load(self.play_file_path + self.play_name)
            self.set_info()
            self.music_length = process_audio.get_music_length(self.play_file_path + self.play_name)
            if self.settings["loop"] == "1":
                pygame.mixer.music.play(loops=-1)
            elif self.settings["loop"] == "0":
                pygame.mixer.music.play()
            self.process.setValue(0)
            print(self.music_length)
            self.process.setMaximum(round(self.music_length))
            self.pp.setIcon(QtGui.QIcon("images\\pause.png"))
            self.timer = QtCore.QBasicTimer()
            self.timer.start(1000, QtCore.Qt.PreciseTimer, self)
            self.result_list(genres)
            self.second = 0
            self.minute = 0
            self.now_genres.setText(genres)
            self.status = 1
            print(self.play_name)

    def next_song(self):
        """
        下一曲槽函数
        :return:
        """
        if self.status != -1 and self.filename:
            self.count += 1
            self.play_time_s.setNum(0)
            self.second = 0
            self.minute = 0
            if self.count < len(self.filename):
                self.play_name = self.filename[self.count]
                pygame.mixer.music.load(self.play_file_path + self.play_name)
                self.set_info()
                self.music_length = process_audio.get_music_length(self.play_file_path + self.play_name)
                if self.settings["loop"] == "1":
                    pygame.mixer.music.play(loops=-1)
                elif self.settings["loop"] == "0":
                    pygame.mixer.music.play()
                self.process.setValue(0)
                print(self.music_length)
                self.process.setMaximum(round(self.music_length))
                self.pp.setIcon(QtGui.QIcon("images\\pause.png"))
                self.timer = QtCore.QBasicTimer()
                self.timer.start(1000, self)
                self.status = 1
                print("下一曲 {}".format(self.play_name))
            else:
                self.count = -1
                print("循环播放")

    def previous_song(self):
        """
        上一曲槽函数
        :return:
        """
        if self.status != -1 and self.filename:
            self.count -= 1
            self.play_time_s.setNum(0)
            self.second = 0
            self.minute = 0
            if self.count >= 0:
                self.play_name = self.filename[self.count]
                pygame.mixer.music.load(self.play_file_path + self.play_name)
                self.set_info()
                if self.settings["loop"] == "1":
                    pygame.mixer.music.play(loops=-1)
                elif self.settings["loop"] == "0":
                    pygame.mixer.music.play()
                self.process.setValue(0)
                print(self.music_length)
                self.process.setMaximum(round(self.music_length))
                self.pp.setIcon(QtGui.QIcon("images\\pause.png"))
                self.timer = QtCore.QBasicTimer()
                self.timer.start(1000, self)
                self.status = 1
                print("上一曲 {}".format(self.play_name))
            else:
                self.count = len(self.filename)
                print("循环播放")

    def change_volume(self, volume):
        """
        修改音量
        :param volume:
        :return:
        """
        pygame.mixer.music.set_volume(volume / 100)

    def set_info(self):
        """
        将音频文件id3信息应用到GUI中
        :return:
        """
        cvr = process_audio.get_cover(self.play_file_path + self.play_name)
        print(cvr)
        info = process_audio.get_song_info(self.play_file_path + self.play_name)
        self.song_name.setText(str(info[0]))
        self.art_abl.setText(str(info[1]) + " - " + str(info[2]))
        self.cover.setPixmap(QtGui.QPixmap(cvr))

    def pp_c(self):
        """
        播放/暂停
        :return:
        """
        if self.status == 1:
            pygame.mixer.music.pause()
            self.pp.setIcon(QtGui.QIcon("images\\play.png"))
            self.timer.stop()
            self.status = 0
            print("暂停")
        elif self.status == 0:
            pygame.mixer.music.unpause()
            self.pp.setIcon(QtGui.QIcon("images\\pause.png"))
            self.timer.start(1000, QtCore.Qt.PreciseTimer, self)
            self.status = 1
            print("播放")

    def loop(self):
        if self.settings["loop"] == "0":
            self.circle.setIcon(QtGui.QIcon("images\\loop_1.png"))
            self.settings["loop"] = "1"
            json.dump(self.settings, open("settings.json", "w"))
        elif self.settings["loop"] == "1":
            self.circle.setIcon(QtGui.QIcon("images\\loop.png"))
            self.settings["loop"] = "0"
            json.dump(self.settings, open("settings.json", "w"))

    def run_cls(self):
        """
        音乐分类槽函数
        :return:
        """
        self.submit.setText("请稍等。。。")
        self.submit.setEnabled(False)
        process_audio.split_audio(file.dir_name(self.dir_path)[1],
                                  file.dir_name(self.dir_path)[0],
                                  self.settings["process_settings"]["sample_rate"],
                                  self.settings["process_settings"]["duration"])

        data = process_audio.get_mfcc(file.dir_name(self.dir_path)[0],
                                      self.settings["process_settings"]["sample_rate"],
                                      self.settings["process_settings"]["duration"],
                                      self.settings["process_settings"]["segments"],
                                      self.settings["process_settings"]["mfcc"],
                                      self.settings["process_settings"]["fft"],
                                      self.settings["process_settings"]["hop_length"])
        predicted = predict.predict("CNN", data, self.settings["genres"])

        file.del_files(file.dir_name(self.dir_path)[0])
        file.del_dir(file.dir_name(self.dir_path)[0])
        file.create_dir(file.dir_name(self.dir_path)[2])
        file.create_genres_dir(file.dir_name(self.dir_path)[2], self.settings["genres"])

        file.move_file(file.dir_name(self.dir_path)[1],
                       file.dir_name(self.dir_path)[2],
                       predicted[0], predicted[1])
        self.submit.setEnabled(True)
        self.submit.setText("已完成！如需继续分类请再次点击")

    def change_settings(self):
        """
        保存设置槽函数
        :return:
        """
        list = ["sample_rate", "duration", "segments", "mfcc", "fft", "hop_length"]
        for i in range(6):
            s = list[i]
            statement = "self." + s + ".text()"
            self.settings["process_settings"][s] = int(eval(statement))
        json.dump(self.settings, open("settings.json", "w"))
        self.submit_settings.setText("已保存！如有更改需要保存设置请再次点击")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Index("I:\\项目\\New_music\\", {"process_settings": {"sample_rate": 22050, "duration": 30, "segments": 10, "mfcc": 13, "fft": 2048, "hop_length": 512}, "genres": ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"], "first_run": "0"})
    win.show()
    sys.exit(app.exec())
