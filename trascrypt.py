from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess
import json 

class Transcryptor:
  def __init__(self, model_name: str) -> None:
    self.sample_rate=16000
    self.model = Model(model_name)
    self.rec = KaldiRecognizer(self.model, self.sample_rate)
    self.cur_res = ""

  def append(self, res) -> None:
    js = json.loads(res)
    if 'text' in js.keys():
      self.cur_res += js['text']
    if 'partial' in js.keys():
      self.cur_res += js['partial']
    self.cur_res += '.\n'

  def transcrypt(self, file_path) -> str:
    self.cur_res = ""
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', file_path, '-ar', str(self.sample_rate),
      '-ac', '1', '-f', 's16le', '-'], stdout=subprocess.PIPE)
    while True:
      data = process.stdout.read(4000)

      if len(data) == 0:
        break
      if self.rec.AcceptWaveform(data):
        self.append(self.rec.Result())
      else:
        print(self.rec.PartialResult())
    self.append(self.rec.FinalResult())

    self.cur_res = self.cur_res[:-2]
    return self.cur_res
