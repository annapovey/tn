from en_norm import tts_norm

 #testing currency
t1 = "thousand"
a1 = "thousand"
assert(tts_norm(t1)==a1)

# t2 = "$3.9 billion"
# a2 = "three point nine billion dollars"
# assert(tts_norm(t2)==a2)

t3 = "75% of children have a life expectancy of under 18."
a3 = "seventy five percent of children have a life expectancy of under eighteen"
#assert(tts_norm(t3)==a3)
# print(tts_norm(t3))

# t4 = "700,000 people"
# a4 = "seven hundred thousand people"
# assert(tts_norm(t4)==a4)

# # t5 = "on 5-6-22 the statistic"
# # a5 = "on May sixth twenty twenty two the statistic"
# # # print(tts_norm(t5))
# # assert(tts_norm(t5)==a5)

# # t6 = "my son is John(III)"
# # a6 = "my son is John three"
# # assert(tts_norm(t6)==a6)

# # t7 = "I got thirty-two on 4-5-21"
# # a7 = "I got thirty two on April fifth twenty twenty one"
# # # print(tts_norm(t7))
# # assert(tts_norm(t7)==a7)

# t8 = "Dr Madam is going at 5 p.m."
# a8 = "Doctor Madam is going at five p m"
# assert(tts_norm(t8)==a8)

# t9 = "I went to the shops and bought ribbons for $3.99, I gave them $5 and they gave me $1.01"
# a9 = "I went to the shops and bought ribbons for three dollars and ninety nine cents I gave them five dollars and they gave me one dollar and one cent"
# assert(tts_norm(t9)==a9)

# print(tts_norm(""))
# # print(tts_norm("Oct. 4 999 january 5th, 1954 in the year 1975 I earned 3412 pounds 4:00"))
# # print(tts_norm("King Alphonso I (reigned 1506-1542) became a devout Roman Catholic.\n\n"))
# # print(tts_norm("striking 1500 kilometres (Fig. 4.4)."))
