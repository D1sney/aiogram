file = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\projects\YourStory\priem_text.txt', 'r', encoding='utf8')
stories = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\projects\YourStory\stories.txt', 'a', encoding='utf8')
photo = file.readline()
stories.write(photo)
stroka = file.readline()
while stroka != '':
    stroka = stroka.rstrip('\n')
    stories.write(f'{stroka} ')
    stroka = file.readline()
stories.write('\n')
file.close()
stories.close()
    