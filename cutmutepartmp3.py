# F:/色々/talkmp3/test.mp3
# F:/色々/talkmp3/cut_test.mp3

from pydub import AudioSegment
from tqdm import tqdm

def cut_audio(input_file, output_file, threshold_db=-30):
    audio = AudioSegment.from_file(input_file)

    # 閾値以下の音量を持つ部分を検出
    parts_to_remove = []
    for i in tqdm(range(len(audio))):
        if audio[i].dBFS < threshold_db:
            if not parts_to_remove or i != parts_to_remove[-1][1] + 1:
                parts_to_remove.append([i, i])
            else:
                parts_to_remove[-1][1] = i

    # 検出された部分を削除
    parts_to_keep = [[0, parts_to_remove[0][0]]]
    for i in tqdm(range(len(parts_to_remove) - 1)):
        parts_to_keep.append([parts_to_remove[i][1] + 1, parts_to_remove[i + 1][0] - 1])
    parts_to_keep.append([parts_to_remove[-1][1] + 1, len(audio) - 1])

    output_audio = AudioSegment.empty()
    for start, end in tqdm(parts_to_keep):
        output_audio += audio[start:end]

    # 出力
    output_audio.export(output_file, format=output_file.split(".")[-1])

# 引数(元ファイル,編集後ファイル,音量の閾値)
cut_audio("F:/色々/talkmp3/wanda.mp3", "F:/色々/talkmp3/cut_test3.mp3", threshold_db=-50)

print("complete!")
