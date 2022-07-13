from en_norm import tts_norm

res = ""
txt_file = open("text.txt")
for line in txt_file:
  res += tts_norm(line)
print(res)
