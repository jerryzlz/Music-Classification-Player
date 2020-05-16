from fct import process_audio, predict, file, verification
import json

settings = json.load(open("settings.json", "r"))

verification.first_run(settings["first_run"])
file.create_dir(file.dir_name(settings["main_settings"]["dir"])[1])
process_audio.split_audio(file.dir_name(settings["main_settings"]["dir"])[1],
                          file.dir_name(settings["main_settings"]["dir"])[0],
                          settings["process_settings"]["sample_rate"],
                          settings["process_settings"]["duration"])
data = process_audio.get_mfcc(file.dir_name(settings["main_settings"]["dir"])[0],
                              settings["process_settings"]["sample_rate"],
                              settings["process_settings"]["duration"],
                              settings["process_settings"]["segments"],
                              settings["process_settings"]["mfcc"],
                              settings["process_settings"]["fft"],
                              settings["process_settings"]["hop_length"])

predicted = predict.predict("CNN", data, settings["genres"])

file.del_files(file.dir_name(settings["main_settings"]["dir"])[0])
file.del_dir(file.dir_name(settings["main_settings"]["dir"])[0])
file.create_dir(settings["main_settings"]["res_dir"])
file.create_genres_dir(settings["main_settings"]["res_dir"], settings["genres"])

file.move_file(file.dir_name(settings["main_settings"]["dir"])[1],
               settings["main_settings"]["res_dir"],
               predicted[0], predicted[1])

print(predicted)

