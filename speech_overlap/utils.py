import re

def clean_subs(subs: list[str]) -> list[str]:
    pass

def parse_time(time_string):
    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])
    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])
    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])
    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])

    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

def parse_srt(srt_string):
    srt_list = []

    for line in srt_string.split('\n\n'):
        if line != '':
            index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+',
                            line).end() + 1
            content = line[pos:]
            start_time_string = re.findall(
                r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            end_time_string = re.findall(
                r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            start_time = parse_time(start_time_string)
            end_time = parse_time(end_time_string)

            srt_list.append({
                'index': index,
                'content': content,
                'start': start_time,
                'end': end_time
            })

    return srt_list

def cuts(i):
  aftercut = []
  parts = [x for x in re.split("[//.|//!|//?]", i['content'])]# if x!=""]
  length = len(i['content']) - i['content'].count('.') - i['content'].count('!') - i['content'].count('?')
  start = i['start']
  end = i['end']

  timedif = end - start
  for j in parts:
    if length != 0:
      proportion = 1 - (length-len(j))/length

      aftercut.append({
          'content': j,
          'time': timedif*proportion
      })
  return aftercut

def translate(translator, sentence):
  eng_content = sentence
  translated_content = []

  #before translator as a parameter  
  #chunk_size, translator = 1000, GoogleTranslator(source='english', target='uk')
  translated_chunk = translator.translate(text=eng_content)
  translated_content.append(translated_chunk)

  compiled_content = '\n'.join(translated_content)
  return(compiled_content)

def millisecond_to_min_millisec(ms:float) -> dict['minute' : int, 'millisecond': int]:
  minutes = int(ms/60000)
  millisecond = int(ms - minutes*60000)
  return {'minute': minutes, 'millisecond': millisecond}