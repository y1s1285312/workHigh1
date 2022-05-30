import discord
from discord.ext import commands
import cv2
import numpy as np
import requests
import pytesseract
from datetime import datetime # 1
from datetime import timedelta
import os

def _ymd_to_datetime(y, m, d):

    s = f'{y:04d}-{m:02d}-{d:02d}'
    return datetime.strptime(s, '%Y-%m-%d')

def week_no(y, m, d):

    target_day = _ymd_to_datetime(y, m, d)  # 4

    firstday =  _ymd_to_datetime(y, 1, 1) # 5
    #print(firstday)
    while firstday.weekday() != 3:  # 6
        firstday += timedelta(days=1)

    return ((target_day - firstday).days // 7) + 2


prefix = "$"
bot = commands.Bot(command_prefix=prefix,help_command= None)
#pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'


@bot.event
async def on_ready():
    """
    This event runs when load the bot or re-load.
    :return: None
    """

    # Define the activity 'Playing A Game' as 'comment'
    game = discord.Game("me")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("READY")


@bot.event
async def on_message(message):
    """
    This event runs when receive message. but It has no restriction of prefix.
    :param message: discord.Message
    :return: None
    """

    # When bot sent message, do nothing.
    if message.author.bot:
        return None

    # Process Commands
    await bot.process_commands(message)

#push item
pushList = {
            '대형보스' : 0,
            '영꺼불': 0,
            '꺼불': 0,
            '경축비': 0,
            '경쿠' : 0,
            '영환불' : 0,
            '놀긍': 0,
            '강환불' :0,
            '반빨별' : 0,
            '반파별' : 0,
            '수큡':0,
            '검환불' :0,
            '태초' : 0,
            '앱솔무기':0,
            '앱솔방어구':0,
            '아케인방어구':0,
            '아케인무기':0,
            '프악스크롤':0,
            '프펫스크롤':0,
            '악세스크롤':0,
            '매지컬':0
                }
findlist=[
    ['대형 보스','메혈 보스','대혈 보스','대형','메혈','대혈'],
    ['영원히','원히','명원히'],
    ['꺼지지','끄지지','깨지지'],
    ['소형','소혈 경험','소혈'],
    ['추가 경험치','추가','주가 경험치','주가'],
    ['영원한','명원한'],
    ['놀라운','놀라문'],
    ['강력한'],
    ['반짝이는 빨간','반짝미는 빨'],
    ['반짝이는 파란','반짝미는 파','반짝미는 바'],
    ['수상한','상한','수삼한'],
    ['검은 환','검믄 환'],
    ['태초의 정수','태초의'],
    ['앱솔랩스 무','맵술랩스 무'],
    ['앱솔랩스 방','맵술랩스 방'],
    ['아케인셰이드 방','마케민셰미드 방','마케인셰미드 방'],
    ['아케인셰이드 무', '마케민셰미드 무', '마케인셰미드 무'],
    ['프리미엄 악','프리미엄 막','프리미멈 악','프리미멈 막'],
    ['프리미엄 펫','프리미엄 펫','프리미멈 펫'],
    ['악세서리 스','막세서리 스'],
    ['매지컬']
]

#순서상관x pushList의 키값이 0번인덱스
addlist = [
        ['영꺼불'],
        ['꺼불'],
        ['수큡','수에큡'],
        ['강환불','강환'],
        ['영환불','영환'],
        ['검환불','검환'],
        ['반파별','반파'],
        ['반빨별','반빨'],
        ['놀긍'],
        ['경축비','경축비','소형경축'],
        ['대형보스','명예','명훈','대형'],
        ['태초','태정'],
        ['경쿠','쿠폰'],
        ['앱솔무기'],
        ['앱솔방어'],
        ['아케인방어구'],
        ['아케인무기'],
        ['프악스크롤'],
        ['프펫스크롤'],
        ['악세스크롤'],
        ['매지컬']


    ]

pushLists={}

def helpmsg (cmdlist):
    helpEmbed = discord.Embed(title = '도움말',color = 0xFFBBC6)
    #print(cmdlist)

    v = cmdlist.pop('{}도움말'.format(prefix))
    #helpEmbed.add_field(name='#도움말', value=v, inline=False)

    for k,v in cmdlist.items():
        helpEmbed.add_field(name=k, value=v,inline=False)

    return helpEmbed

@bot.command(name="도움말",description = '{}도움말'.format(prefix) , help = '도움말 출력')
async def help(ctx):
    cmdlist= {}
    for cmd in bot.commands :
        cmdlist[cmd.description] = cmd.help

    Embed = helpmsg(cmdlist)
    await ctx.channel.send(embed = Embed)
    return None

@bot.command(name="수에큡",description = '{}수에큡'.format(prefix) , help = '하드보스 수에큡 갯수')
async def cube(ctx,name=''):
    cubeList = {
        '진힐라': 10,
        '듄켈': 10,
        '더스크': 10,
        '윌': 9,
        '루시드': 9,
        '스우': 8,
        '데미안': 7
    }
    msgs = ''

    if name =='':
        for k,v in cubeList.items():
            msg = '{} {}개\n'.format(k,v)
            msgs += msg
    else:
        try:
            msgs = '{} {}개\n'.format(name,cubeList[name])
        except:
            return None

    await ctx.channel.send(msgs)
    return None


@bot.command(name="cls",description = '{}cls'.format(prefix) , help = '추출한 아이템 목록 초기화')
async def c(ctx):
    id = ctx.guild.id
    pushLists[id] = pushList.copy()
    return None

@bot.command(name="add", description = '{}add (아이템명) (수량)'.format(prefix),help=
'''
추출 아이템 목록에서 (아이템명)의 갯수를 (수량)만큼 더함
#추가 만 입력할경우 유요한 (아이템명)이 출력된다
''')
async def push(ctx,*itemlist):
    #print(itemlist)

    msgs = ''
    for item in addlist:
        msg = item[0]+'\t=\t'+','.join(item[1:]) + '\n'
        msgs += msg

    if len(itemlist) ==0 :
        await ctx.channel.send("## 아이템 목록 ##\n"+msgs)
        return None

    id = ctx.guild.id
    print(id)
    if id not in list(pushLists.keys()) :
        pushLists[id] = pushList.copy()

    keys = [x for x in itemlist if not x.lstrip("-").isdigit()]
    vals = [int(x) for x in itemlist if x.lstrip("-").isdigit()]

    for key in keys:
        #if key not in list(pushLists[id].keys()):
        if key not in msgs:
            await ctx.channel.send("잘못된 아이템 이름\n아이템 목록 보기 : #추가")
            return None

    for i,k in enumerate(keys):
        for j, item in enumerate(addlist):
            #print(item)
            if k in item:
                #print('아이템추가',item[0])
                pushLists[id][item[0]] += vals[i]
                if pushLists[id][item[0]] < 0:
                    pushLists[id][item[0]] = 0
                break
    '''          
    for i, item in enumerate(keys):
        pushLists[id][item] += vals[i]
        if pushLists[id][item] < 0:
            pushLists[id][item]=0
    '''
    return None

@bot.command(name="dis",description = '{}dis'.format(prefix) , help='획득한 여러 아이템을 인원수에 따라 n빵')
async def printData(ctx,num=2):
    id = ctx.guild.id
    print(id)
    chnid = None
    if ctx.message.channel.name != '분배':
        for x in ctx.guild.text_channels:
            if x.name == '분배':
                chnid = x.id

    num = int(num)
    if id not in list(pushLists.keys()) :
        pushLists[id] = pushList.copy()

    #now = datetime.now()
    #target = week_no(now.year,now.month,now.day)
    #msg = "##### 분배 #####".format(target)
    #await ctx.channel.send(msg)
    now = datetime.now()
    target = week_no(now.year, now.month, now.day)
    msg = ''
    #msg = "##### {} 주차 #####\n".format(target)
    #msgs = msg+'##### 분배 #####\n'
    msgs=''
    Embed = discord.Embed(title='{}주차'.format(target), color=0xFFBBC6)

    exlist = {}
    for k, v in pushLists[id].items():
        if v > 0:
            if (v//num) > 0 :
                msg = '{} {} \n'.format(k,v // num)
                msgs += msg
            if v%num > 0 :
                exlist[k] = v%num



    if msgs != '':
        Embed.add_field(name='분배', value=msgs, inline=True)
        #await ctx.channel.send(embed=Embed)


    msgs = ''
    for k,v in exlist.items():
        msg = '{} {}\n'.format(k, v)
        msgs+=msg

    pushLists[id]=exlist

    if msgs != '':
        #msgs = '##### 나머지 #####\n'+msgs
        Embed.add_field(name='나머지', value=msgs, inline=True)
        await ctx.channel.send(embed=Embed)
        if chnid != None:
            await bot.get_channel(chnid).send(embed=Embed)

    return None

@bot.command(name="ls",description = '{}ls'.format(prefix) , help='추출한 아이템들을 누적해서 총 갯수를 보여준다')
async def printData(ctx):
    id = ctx.guild.id

    #print(ctx.guild.text_channels)
    chnid = None
    if ctx.message.channel.name !='정산':
        for x in ctx.guild.text_channels:
            if x.name == '정산':
                chnid = x.id



    if id not in list(pushLists.keys()) :
        pushLists[id] = pushList.copy()


    now = datetime.now()
    target = week_no(now.year,now.month,now.day)

    msg = ''
    #msg = "##### {} 주차 #####\n".format(target)
    # await ctx.channel.send(msg)

    Embed = discord.Embed(title='{}주차'.format(target), color=0xFFBBC6)

    for k, v in pushLists[id].items():
        if v > 0:
            msg += '{} {}\n'.format(k, v)
            #msg += '{} {} \t\t 분배 : {} 나머지 : {}\n'.format(k, v,v//2,v%2)



    if msg != '':
        Embed.add_field(name='합계', value=msg, inline=True)
        await ctx.channel.send(embed = Embed)
        if chnid != None:
            await bot.get_channel(chnid).send(embed=Embed)

    return None


#item search
@bot.command(name="get",description ='{}get (캡처이미지)'.format(prefix)
            , help='''
            (캡처이미지)에서 아이템추출 (누적)
            (캡처이미지) :
            1. 메이플 해상도 1366x768 기준.
            2. 채팅창의 세로는 최대, 가로는 최소크기로 한다.
            3. Window키 + 쉬프트 + s 키를 눌러서 메이플 창을 캡처한다.
            4. 한번에 캡처가 불가능할경우 겹치지않게 여러장으로 캡처해서 올린다.
            ''')
async def ls(ctx):
    itemList = pushList.copy()
    id = ctx.guild.id
    order = []
    if id not in list(pushLists.keys()) :
        pushLists[id] = pushList.copy()

    for img in ctx.message.attachments:
        print(img.url)

        url = img.url
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        image = cv2.imdecode(image_nparray, cv2.IMREAD_GRAYSCALE)

        height, width = image.shape

        if (height == 795 or height==768)  and (width == 1368 or width==1366):
            image = image[height-528:height-17,5:150]
            #cv2.imshow('Image from url', image)
            #cv2.waitKey(0)
        else :

            des = '''
            1. 메이플 해상도 1366x768 기준.
            2. 채팅창의 세로는 최대, 가로는 최소크기로 한다.
            3. Window키 + 쉬프트 + s 키를 눌러서 메이플 창을 캡처한다.
            '''
            embed = discord.Embed(title="옳바른 이미지 캡처", description= des,clolr=0x00ff56)
            #embed.set_image(url='https://cdn.discordapp.com/attachments/960404850275938357/961516665084969031/testimg.png')

            await ctx.channel.send(embed =embed)
            return None

        bordersize = 20
        border = cv2.copyMakeBorder(
            image,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0]
        )

        #height, width = org.shape
        height, width = border.shape
        #image = cv2.resize(border, (width*2,height*2), interpolation=cv2.INTER_LINEAR)
        #image = cv2.resize(org, (4000,5000), interpolation=cv2.INTER_LINEAR)

        ret, result = cv2.threshold(border, 130, 255, cv2.THRESH_BINARY)

        result = cv2.bitwise_not(result)

        result = cv2.resize(result, (width *3, height *3), interpolation=cv2.INTER_LINEAR)

        #cv2.imshow('Image from url', result)
        #cv2.waitKey(0)

        text = pytesseract.image_to_string(result, lang='kor',config='--oem 1 --psm 6 -c preserve_interword_spaces=1')
        #print(text)
        text = text.split('\n')
        text = list(filter((lambda x: len(x) > 10), text))

        exlist= ['루나','십자','강렬','뒤틀린','파워','수상한','수삼한','파뭐']

        for x in text:
            isEx = False
            for ex in exlist:
                if ex in x:
                    isEx=True
                    break
            if not isEx:
                print(x)




        for item in text:
            for i,finds in enumerate(findlist):
                isfind = False
                for find in finds:
                    if find in item:
                        if i != 10:
                            print(i,end=' ')
                            print(list(pushList.keys())[i])
                        key = list(pushList.keys())[i]
                        pushLists[id][key]+=1
                        itemList[key]+=1
                        if key not in order:
                            order.append(key)
                        isfind = True
                        break
                if isfind:
                    break

    msg = ''
    '''
    for k, v in itemList.items():
        if v > 0:
            msg += '{} {}\n'.format(k, v)
    '''
    for k in order:
        if  itemList[k]> 0:
            msg += '{} {}\n'.format(k, itemList[k])

    if msg:
        await ctx.channel.send(msg)

    return None


#calc
@bot.command(name="cal",description='{}cal (메소)'.format(prefix),help=
'''
수수료 감안해서 (메소)를 n빵 
경매장에서 판매완료한 아이템들의 총 금액 입력하면 인원수에 따라 메소를 분배한다
주는금액 : 한명에게 분배해줄 메소(분배한 메소의 수수료(3%)를 제외한 메소)
남은금액 : 분배한 사람이 n명에게 분배해주고 남은 메소
'''
             )
async def calc(ctx,total='',num='2'):
    if total == '' or (not total.isdigit()) or int(total) < 1 or (not num.isdigit()):
        #print('total x')
        msg = '사용법 : # (총액)'
        await ctx.channel.send(msg)
        return None
    print('calc {}'.format(total))

    num = int(num)

    fRate = (num*100) / (num*100-3)

    print(fRate)
    result = int(total) / num
    result = result * fRate
    result = int(result)

    msg = "주는금액: {}({}) \n남은금액: {}".format(format(result, ','), format(int(result * 0.97), ','),
                                           format(int(total) - result*(num-1), ','))

    await ctx.channel.send(msg)
    return None

@bot.command(name="ip",description='{}cal (메소)'.format(prefix),help=
'''

'''
             )
async def calc(ctx,total='',num='2'):
    await ctx.channel.send('search ip')


# Referencing token in Json file and run the bot.
bot.run(os.environ.get('TOKEN'))
#bot.run('OTU5ODg0MTg0MTcwNjY4MDYy.YkiXzw.B_rPRmLKN7PtiVnJmE5jCd4H5zQ')

