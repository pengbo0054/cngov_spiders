import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import jieba
 
text_from_file_with_apath = open('lz.txt').read()
 
wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
wl_space_split = " ".join(wordlist_after_jieba)
cloud_mask = imread("back2.jpg")
my_wordcloud = WordCloud(font_path="STHeiti Medium.ttc",background_color='white',mask=cloud_mask,max_words=50,max_font_size=100)
image_colors = ImageColorGenerator(cloud_mask)

my_wordcloud.generate(wl_space_split)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(cloud_mask)

plt.figure()
# 以下代码显示图片
plt.imshow(my_wordcloud)
plt.axis("off")
#plt.show()
# 绘制词云
image_colors = ImageColorGenerator(cloud_mask)

plt.imshow(my_wordcloud.recolor(color_func=image_colors))
#plt.axis("off")
# 绘制背景图片为颜色的图片
#plt.figure()
#plt.imshow(cloud_mask, cmap=plt.cm.gray)
#plt.axis("off")
plt.show()

