import tkinter as tk
from gtts import gTTS
import os
import pygame
from pygame import mixer
import time

# Inicializar o mixer do pygame para reproduzir áudio
mixer.init()

# Lista de palavras do HSK 1 com múltiplos exemplos
words = [
    {
        "ideogram": "爱",
        "pinyin": "ài",
        "translation": "Amar",
        "examples": [
            "我爱妈妈。 (Wǒ ài māma.) (Eu amo a mamãe.)",
            "我爱学习汉语。 (Wǒ ài xuéxí Hànyǔ.) (Eu amo estudar chinês.)",
            "我爱中国。 (Wǒ ài Zhōngguó.) (Eu amo a China.)"
        ]
    },
    {
        "ideogram": "爸爸",
        "pinyin": "bà ba",
        "translation": "Pai",
        "examples": [
            "我爸爸是老师。 (Wǒ bàba shì lǎoshī.) (Meu pai é professor.)",
            "爸爸在做饭。 (Bàba zài zuòfàn.) (Papai está cozinhando.)",
            "爸爸喜欢喝茶。 (Bàba xǐhuān hē chá.) (Papai gosta de beber chá.)"
        ]
    },
    {
        "ideogram": "杯子",
        "pinyin": "bēi zi",
        "translation": "Copo",
        "examples": [
            "这是一个杯子。 (Zhè shì yīgè bēizi.) (Isso é um copo.)",
            "杯子里有水。 (Bēizi lǐ yǒu shuǐ.) (Tem água no copo.)",
            "请给我一个杯子。 (Qǐng gěi wǒ yīgè bēizi.) (Por favor, me dê um copo.)"
        ]
    },
    {
        "ideogram": "北京",
        "pinyin": "Běi jīng",
        "translation": "Pequim",
        "examples": [
            "我去北京。 (Wǒ qù Běijīng.) (Eu vou para Pequim.)",
            "北京很漂亮。 (Běijīng hěn piàoliang.) (Pequim é muito bonita.)",
            "北京有很多人。 (Běijīng yǒu hěn duō rén.) (Pequim tem muitas pessoas.)"
        ]
    },
    {
        "ideogram": "本",
        "pinyin": "běn",
        "translation": "Volume (livro)",
        "examples": [
            "这本书很好。 (Zhè běn shū hěn hǎo.) (Este livro é muito bom.)",
            "我买了一本书。 (Wǒ mǎile yī běn shū.) (Eu comprei um livro.)",
            "你有几本书？ (Nǐ yǒu jǐ běn shū?) (Quantos livros você tem?)"
        ]
    },
    {
        "ideogram": "不",
        "pinyin": "bù",
        "translation": "Não",
        "examples": [
            "我不去。 (Wǒ bù qù.) (Eu não vou.)",
            "他不喜欢咖啡。 (Tā bù xǐhuān kāfēi.) (Ele não gosta de café.)",
            "这不是我的书。 (Zhè bù shì wǒ de shū.) (Este não é o meu livro.)"
        ]
    },
    {
        "ideogram": "不客气",
        "pinyin": "bù kè qi",
        "translation": "De nada",
        "examples": [
            "不客气！ (Bù kèqi!) (De nada!)",
            "谢谢你的帮助！不客气！ (Xièxiè nǐ de bāngzhù! Bù kèqi!) (Obrigado pela ajuda! De nada!)",
            "不客气，这是我的工作。 (Bù kèqi, zhè shì wǒ de gōngzuò.) (De nada, este é o meu trabalho.)"
        ]
    },
    {
        "ideogram": "菜",
        "pinyin": "cài",
        "translation": "Prato (comida)",
        "examples": [
            "这个菜很好吃。 (Zhège cài hěn hǎo chī.) (Este prato é muito gostoso.)",
            "我喜欢吃中国菜。 (Wǒ xǐhuān chī Zhōngguó cài.) (Eu gosto de comer comida chinesa.)",
            "妈妈做的菜很棒。 (Māma zuò de cài hěn bàng.) (A comida que a mamãe faz é ótima.)"
        ]
    },
    {
        "ideogram": "茶",
        "pinyin": "chá",
        "translation": "Chá",
        "examples": [
            "我喜欢喝茶。 (Wǒ xǐhuān hē chá.) (Eu gosto de beber chá.)",
            "请给我一杯茶。 (Qǐng gěi wǒ yī bēi chá.) (Por favor, me dê uma xícara de chá.)",
            "这是绿茶。 (Zhè shì lǜchá.) (Este é chá verde.)"
        ]
    },
    {
        "ideogram": "吃",
        "pinyin": "chī",
        "translation": "Comer",
        "examples": [
            "我吃米饭。 (Wǒ chī mǐfàn.) (Eu como arroz.)",
            "你吃早饭了吗？ (Nǐ chī zǎofàn le ma?) (Você já tomou café da manhã?)",
            "我们一起吃晚饭吧。 (Wǒmen yīqǐ chī wǎnfàn ba.) (Vamos jantar juntos.)"
        ]
    },
    {
        "ideogram": "出租车",
        "pinyin": "chū zū chē",
        "translation": "Táxi",
        "examples": [
            "我坐出租车去。 (Wǒ zuò chūzūchē qù.) (Eu vou de táxi.)",
            "出租车司机很好。 (Chūzūchē sījī hěn hǎo.) (O motorista de táxi é muito bom.)",
            "请叫一辆出租车。 (Qǐng jiào yī liàng chūzūchē.) (Por favor, chame um táxi.)"
        ]
    },
    {
        "ideogram": "打电话",
        "pinyin": "dǎ diàn huà",
        "translation": "Telefonar",
        "examples": [
            "我给妈妈打电话。 (Wǒ gěi māma dǎ diànhuà.) (Eu telefono para a mamãe.)",
            "他正在打电话。 (Tā zhèngzài dǎ diànhuà.) (Ele está telefonando.)",
            "请打电话给我。 (Qǐng dǎ diànhuà gěi wǒ.) (Por favor, me ligue.)"
        ]
    },
    {
        "ideogram": "大",
        "pinyin": "dà",
        "translation": "Grande",
        "examples": [
            "这个房子很大。 (Zhège fángzi hěn dà.) (Esta casa é muito grande.)",
            "大象很大。 (Dàxiàng hěn dà.) (O elefante é muito grande.)",
            "中国是一个大国。 (Zhōngguó shì yīgè dà guó.) (A China é um país grande.)"
        ]
    },
    {
        "ideogram": "的",
        "pinyin": "de",
        "translation": "Partícula possessiva",
        "examples": [
            "这是我的书。 (Zhè shì wǒ de shū.) (Este é o meu livro.)",
            "他的车很贵。 (Tā de chē hěn guì.) (O carro dele é muito caro.)",
            "你喜欢吃什么的水果？ (Nǐ xǐhuān chī shénme de shuǐguǒ?) (Que tipo de fruta você gosta de comer?)"
        ]
    },
    {
        "ideogram": "点",
        "pinyin": "diǎn",
        "translation": "Ponto, hora",
        "examples": [
            "现在三点。 (Xiànzài sān diǎn.) (Agora são três horas.)",
            "我们几点见面？ (Wǒmen jǐ diǎn jiànmiàn?) (A que horas nos encontramos?)",
            "请给我一点时间。 (Qǐng gěi wǒ yīdiǎn shíjiān.) (Por favor, me dê um pouco de tempo.)"
        ]
    },
    {
        "ideogram": "电脑",
        "pinyin": "diàn nǎo",
        "translation": "Computador",
        "examples": [
            "我用电脑工作。 (Wǒ yòng diànnǎo gōngzuò.) (Eu uso o computador para trabalhar.)",
            "这是新电脑。 (Zhè shì xīn diànnǎo.) (Este é um computador novo.)",
            "电脑坏了。 (Diànnǎo huàile.) (O computador quebrou.)"
        ]
    },
    {
        "ideogram": "电视",
        "pinyin": "diàn shì",
        "translation": "Televisão",
        "examples": [
            "我看电视。 (Wǒ kàn diànshì.) (Eu assisto televisão.)",
            "电视节目很有趣。 (Diànshì jiémù hěn yǒuqù.) (O programa de TV é muito interessante.)",
            "请打开电视。 (Qǐng dǎkāi diànshì.) (Por favor, ligue a TV.)"
        ]
    },
        {
        "ideogram": "电影",
        "pinyin": "diàn yǐng",
        "translation": "Filme",
        "examples": [
            "我喜欢看电影。 (Wǒ xǐhuān kàn diànyǐng.) (Eu gosto de assistir filmes.)",
            "这部电影很有趣。 (Zhè bù diànyǐng hěn yǒuqù.) (Este filme é muito interessante.)",
            "我们去看电影吧。 (Wǒmen qù kàn diànyǐng ba.) (Vamos assistir a um filme.)"
        ]
    },
    {
        "ideogram": "东西",
        "pinyin": "dōng xi",
        "translation": "Coisa",
        "examples": [
            "这是什么东西？ (Zhè shì shénme dōngxi?) (O que é isso?)",
            "我买了很多东西。 (Wǒ mǎile hěn duō dōngxi.) (Eu comprei muitas coisas.)",
            "这个东西很贵。 (Zhège dōngxi hěn guì.) (Esta coisa é muito cara.)"
        ]
    },
    {
        "ideogram": "都",
        "pinyin": "dōu",
        "translation": "Todos",
        "examples": [
            "我们都去。 (Wǒmen dōu qù.) (Todos nós vamos.)",
            "他们都喜欢喝茶。 (Tāmen dōu xǐhuān hē chá.) (Todos eles gostam de beber chá.)",
            "这些书都很好。 (Zhèxiē shū dōu hěn hǎo.) (Todos esses livros são muito bons.)"
        ]
    },
    {
        "ideogram": "读",
        "pinyin": "dú",
        "translation": "Ler",
        "examples": [
            "我读书。 (Wǒ dú shū.) (Eu leio livros.)",
            "他喜欢读报纸。 (Tā xǐhuān dú bàozhǐ.) (Ele gosta de ler jornal.)",
            "请读这个句子。 (Qǐng dú zhège jùzi.) (Por favor, leia esta frase.)"
        ]
    },
    {
        "ideogram": "对不起",
        "pinyin": "duì bu qǐ",
        "translation": "Desculpe",
        "examples": [
            "对不起，我迟到了。 (Duìbuqǐ, wǒ chídào le.) (Desculpe, eu me atrasei.)",
            "对不起，我忘了。 (Duìbuqǐ, wǒ wàngle.) (Desculpe, eu esqueci.)",
            "对不起，这是我的错。 (Duìbuqǐ, zhè shì wǒ de cuò.) (Desculpe, isso foi minha culpa.)"
        ]
    },
    {
        "ideogram": "多",
        "pinyin": "duō",
        "translation": "Muito",
        "examples": [
            "这里有很多人。 (Zhèlǐ yǒu hěn duō rén.) (Há muitas pessoas aqui.)",
            "你多大了？ (Nǐ duō dà le?) (Quantos anos você tem?)",
            "请多给我一点时间。 (Qǐng duō gěi wǒ yīdiǎn shíjiān.) (Por favor, me dê um pouco mais de tempo.)"
        ]
    },
    {
        "ideogram": "多少",
        "pinyin": "duō shao",
        "translation": "Quanto",
        "examples": [
            "这个多少钱？ (Zhège duōshǎo qián?) (Quanto custa isso?)",
            "你有多少书？ (Nǐ yǒu duōshǎo shū?) (Quantos livros você tem?)",
            "这里有多少人？ (Zhèlǐ yǒu duōshǎo rén?) (Quantas pessoas há aqui?)"
        ]
    },
    {
        "ideogram": "儿子",
        "pinyin": "ér zi",
        "translation": "Filho",
        "examples": [
            "我有一个儿子。 (Wǒ yǒu yīgè érzi.) (Eu tenho um filho.)",
            "我儿子很聪明。 (Wǒ érzi hěn cōngmíng.) (Meu filho é muito inteligente.)",
            "他儿子是医生。 (Tā érzi shì yīshēng.) (O filho dele é médico.)"
        ]
    },
    {
        "ideogram": "二",
        "pinyin": "èr",
        "translation": "Dois",
        "examples": [
            "我有两个苹果。 (Wǒ yǒu liǎng gè píngguǒ.) (Eu tenho duas maçãs.)",
            "这是二月的第二天。 (Zhè shì èr yuè de dì èr tiān.) (Este é o segundo dia de fevereiro.)",
            "二加二等于四。 (Èr jiā èr děngyú sì.) (Dois mais dois é igual a quatro.)"
        ]
    },
    {
        "ideogram": "饭店",
        "pinyin": "fàn diàn",
        "translation": "Restaurante",
        "examples": [
            "我们去饭店吃饭。 (Wǒmen qù fàndiàn chīfàn.) (Nós vamos ao restaurante comer.)",
            "这家饭店很好吃。 (Zhè jiā fàndiàn hěn hǎo chī.) (Este restaurante é muito gostoso.)",
            "饭店里有很多人。 (Fàndiàn lǐ yǒu hěn duō rén.) (Há muitas pessoas no restaurante.)"
        ]
    },
    {
        "ideogram": "飞机",
        "pinyin": "fēi jī",
        "translation": "Avião",
        "examples": [
            "我坐飞机去北京。 (Wǒ zuò fēijī qù Běijīng.) (Eu vou para Pequim de avião.)",
            "飞机晚点了。 (Fēijī wǎndiǎn le.) (O avião está atrasado.)",
            "这是第一次坐飞机。 (Zhè shì dì yī cì zuò fēijī.) (Esta é a primeira vez que eu viajo de avião.)"
        ]
    },
    {
        "ideogram": "分钟",
        "pinyin": "fēn zhōng",
        "translation": "Minuto",
        "examples": [
            "我等了十分钟。 (Wǒ děngle shí fēnzhōng.) (Eu esperei dez minutos.)",
            "还有五分钟。 (Hái yǒu wǔ fēnzhōng.) (Faltam cinco minutos.)",
            "请等我一分钟。 (Qǐng děng wǒ yī fēnzhōng.) (Por favor, espere um minuto.)"
        ]
    },
    {
        "ideogram": "高兴",
        "pinyin": "gāo xìng",
        "translation": "Feliz",
        "examples": [
            "我很高兴。 (Wǒ hěn gāoxìng.) (Eu estou muito feliz.)",
            "他高兴地笑了。 (Tā gāoxìng de xiào le.) (Ele sorriu feliz.)",
            "今天是个高兴的日子。 (Jīntiān shì gè gāoxìng de rìzi.) (Hoje é um dia feliz.)"
        ]
    },

    {
        "ideogram": "个",
        "pinyin": "gè",
        "translation": "Unidade (classificador)",
        "examples": [
            "一个人 (Yīgè rén) (Uma pessoa)",
            "三个苹果 (Sān gè píngguǒ) (Três maçãs)",
            "你有几个兄弟姐妹？ (Nǐ yǒu jǐ gè xiōngdì jiěmèi?) (Quantos irmãos você tem?)"
        ]
    },

    {
        "ideogram": "工作",
        "pinyin": "gōng zuò",
        "translation": "Trabalho",
        "examples": [
            "我去工作。 (Wǒ qù gōngzuò.) (Eu vou trabalhar.)",
            "他找到新工作了。 (Tā zhǎodào xīn gōngzuò le.) (Ele encontrou um novo trabalho.)",
            "工作很忙。 (Gōngzuò hěn máng.) (O trabalho está muito ocupado.)"
        ]
    },    {
        "ideogram": "狗",
        "pinyin": "gǒu",
        "translation": "Cachorro",
        "examples": [
            "这只狗很可爱。 (Zhè zhī gǒu hěn kě'ài.) (Este cachorro é muito fofo.)",
            "我有一只狗。 (Wǒ yǒu yī zhī gǒu.) (Eu tenho um cachorro.)",
            "狗在叫。 (Gǒu zài jiào.) (O cachorro está latindo.)"
        ]
    },
    {
        "ideogram": "汉语",
        "pinyin": "Hàn yǔ",
        "translation": "Língua chinesa",
        "examples": [
            "我学习汉语。 (Wǒ xuéxí Hànyǔ.) (Eu estudo chinês.)",
            "汉语很难。 (Hànyǔ hěn nán.) (O chinês é muito difícil.)",
            "你会说汉语吗？ (Nǐ huì shuō Hànyǔ ma?) (Você sabe falar chinês?)"
        ]
    },
    {
        "ideogram": "好",
        "pinyin": "hǎo",
        "translation": "Bom",
        "examples": [
            "你好！ (Nǐ hǎo!) (Olá!)",
            "这个主意很好。 (Zhège zhǔyì hěn hǎo.) (Esta ideia é muito boa.)",
            "今天天气很好。 (Jīntiān tiānqì hěn hǎo.) (O tempo está muito bom hoje.)"
        ]
    },
    {
        "ideogram": "号",
        "pinyin": "hào",
        "translation": "Número",
        "examples": [
            "我的电话号码是123456。 (Wǒ de diànhuà hàomǎ shì 123456.) (Meu número de telefone é 123456.)",
            "这是几号？ (Zhè shì jǐ hào?) (Que dia é hoje?)",
            "请记住这个号码。 (Qǐng jìzhù zhège hàomǎ.) (Por favor, lembre-se deste número.)"
        ]
    },
    {
        "ideogram": "喝",
        "pinyin": "hē",
        "translation": "Beber",
        "examples": [
            "我喝水。 (Wǒ hē shuǐ.) (Eu bebo água.)",
            "你喜欢喝咖啡吗？ (Nǐ xǐhuān hē kāfēi ma?) (Você gosta de beber café?)",
            "请喝一杯茶。 (Qǐng hē yī bēi chá.) (Por favor, tome uma xícara de chá.)"
        ]
    },
    {
        "ideogram": "和",
        "pinyin": "hé",
        "translation": "E",
        "examples": [
            "我和你一起去。 (Wǒ hé nǐ yīqǐ qù.) (Eu vou com você.)",
            "我喜欢茶和咖啡。 (Wǒ xǐhuān chá hé kāfēi.) (Eu gosto de chá e café.)",
            "这是我和他的书。 (Zhè shì wǒ hé tā de shū.) (Este é o livro dele e meu.)"
        ]
    },
    {
        "ideogram": "很",
        "pinyin": "hěn",
        "translation": "Muito",
        "examples": [
            "很好 (Hěn hǎo) (Muito bom)",
            "他很高兴。 (Tā hěn gāoxìng.) (Ele está muito feliz.)",
            "这本书很有趣。 (Zhè běn shū hěn yǒuqù.) (Este livro é muito interessante.)"
        ]
    },
    {
        "ideogram": "后面",
        "pinyin": "hòu miàn",
        "translation": "Atrás",
        "examples": [
            "他在后面。 (Tā zài hòumiàn.) (Ele está atrás.)",
            "请坐在后面。 (Qǐng zuò zài hòumiàn.) (Por favor, sente-se atrás.)",
            "房子后面有一个花园。 (Fángzi hòumiàn yǒu yīgè huāyuán.) (Há um jardim atrás da casa.)"
        ]
    },
    {
        "ideogram": "回",
        "pinyin": "huí",
        "translation": "Voltar",
        "examples": [
            "我回家。 (Wǒ huí jiā.) (Eu volto para casa.)",
            "他明天回北京。 (Tā míngtiān huí Běijīng.) (Ele volta para Pequim amanhã.)",
            "请回电话给我。 (Qǐng huí diànhuà gěi wǒ.) (Por favor, me retorne a ligação.)"
        ]
    },
    {
        "ideogram": "会",
        "pinyin": "huì",
        "translation": "Saber",
        "examples": [
            "我会说汉语。 (Wǒ huì shuō Hànyǔ.) (Eu sei falar chinês.)",
            "你会开车吗？ (Nǐ huì kāichē ma?) (Você sabe dirigir?)",
            "他不会游泳。 (Tā bù huì yóuyǒng.) (Ele não sabe nadar.)"
        ]
    },
    {
        "ideogram": "几",
        "pinyin": "jǐ",
        "translation": "Quantos",
        "examples": [
            "你几岁？ (Nǐ jǐ suì?) (Quantos anos você tem?)",
            "现在几点？ (Xiànzài jǐ diǎn?) (Que horas são agora?)",
            "你有几个朋友？ (Nǐ yǒu jǐ gè péngyou?) (Quantos amigos você tem?)"
        ]
    },
    {
        "ideogram": "家",
        "pinyin": "jiā",
        "translation": "Casa",
        "examples": [
            "我回家。 (Wǒ huí jiā.) (Eu volto para casa.)",
            "这是我家。 (Zhè shì wǒ jiā.) (Esta é a minha casa.)",
            "你家在哪里？ (Nǐ jiā zài nǎlǐ?) (Onde fica a sua casa?)"
        ]
    },
    {
        "ideogram": "叫",
        "pinyin": "jiào",
        "translation": "Chamar",
        "examples": [
            "你叫什么名字？ (Nǐ jiào shénme míngzì?) (Qual é o seu nome?)",
            "他叫小明。 (Tā jiào Xiǎo Míng.) (Ele se chama Xiao Ming.)",
            "请叫我明天。 (Qǐng jiào wǒ míngtiān.) (Por favor, me chame amanhã.)"
        ]
    },
    {
        "ideogram": "今天",
        "pinyin": "jīn tiān",
        "translation": "Hoje",
        "examples": [
            "今天天气很好。 (Jīntiān tiānqì hěn hǎo.) (O tempo está muito bom hoje.)",
            "今天是我的生日。 (Jīntiān shì wǒ de shēngrì.) (Hoje é o meu aniversário.)",
            "今天我们去公园。 (Jīntiān wǒmen qù gōngyuán.) (Hoje vamos ao parque.)"
        ]
    },
    {
        "ideogram": "九",
        "pinyin": "jiǔ",
        "translation": "Nove",
        "examples": [
            "九个人 (Jiǔ gè rén) (Nove pessoas)",
            "现在是九点。 (Xiànzài shì jiǔ diǎn.) (Agora são nove horas.)",
            "我买了九本书。 (Wǒ mǎile jiǔ běn shū.) (Eu comprei nove livros.)"
        ]
    },
    {
        "ideogram": "开",
        "pinyin": "kāi",
        "translation": "Abrir",
        "examples": [
            "开门 (Kāi mén) (Abrir a porta)",
            "请开灯。 (Qǐng kāi dēng.) (Por favor, acenda a luz.)",
            "他开了一家店。 (Tā kāile yī jiā diàn.) (Ele abriu uma loja.)"
        ]
    },
    {
        "ideogram": "看",
        "pinyin": "kàn",
        "translation": "Ver",
        "examples": [
            "我看电视。 (Wǒ kàn diànshì.) (Eu assisto televisão.)",
            "你看这本书吗？ (Nǐ kàn zhè běn shū ma?) (Você está lendo este livro?)",
            "请看清楚。 (Qǐng kàn qīngchǔ.) (Por favor, veja com atenção.)"
        ]
    },
    {
        "ideogram": "看见",
        "pinyin": "kàn jiàn",
        "translation": "Ver",
        "examples": [
            "我看见一只猫。 (Wǒ kànjiàn yī zhī māo.) (Eu vejo um gato.)",
            "你看见我的书了吗？ (Nǐ kànjiàn wǒ de shū le ma?) (Você viu o meu livro?)",
            "他看见了我。 (Tā kànjiànle wǒ.) (Ele me viu.)"
        ]
    },
    {
        "ideogram": "块",
        "pinyin": "kuài",
        "translation": "Unidade monetária",
        "examples": [
            "十块钱 (Shí kuài qián) (Dez yuan)",
            "这个多少钱？五块。 (Zhège duōshǎo qián? Wǔ kuài.) (Quanto custa isso? Cinco yuan.)",
            "我只有一百块。 (Wǒ zhǐ yǒu yībǎi kuài.) (Eu só tenho cem yuan.)"
        ]
    },
    {
        "ideogram": "来",
        "pinyin": "lái",
        "translation": "Vir",
        "examples": [
            "我来中国。 (Wǒ lái Zhōngguó.) (Eu venho para a China.)",
            "请来我家。 (Qǐng lái wǒ jiā.) (Por favor, venha à minha casa.)",
            "他明天来。 (Tā míngtiān lái.) (Ele vem amanhã.)"
        ]
    },
    {
        "ideogram": "老师",
        "pinyin": "lǎo shī",
        "translation": "Professor",
        "examples": [
            "我的老师很好。 (Wǒ de lǎoshī hěn hǎo.) (Meu professor é muito bom.)",
            "他是我的老师。 (Tā shì wǒ de lǎoshī.) (Ele é meu professor.)",
            "老师教我们汉语。 (Lǎoshī jiāo wǒmen Hànyǔ.) (O professor nos ensina chinês.)"
        ]
    },
    {
        "ideogram": "了",
        "pinyin": "le",
        "translation": "Partícula de aspecto",
        "examples": [
            "我吃了。 (Wǒ chī le.) (Eu comi.)",
            "他去了北京。 (Tā qùle Běijīng.) (Ele foi para Pequim.)",
            "我明白了。 (Wǒ míngbái le.) (Eu entendi.)"
        ]
    },
    {
        "ideogram": "冷",
        "pinyin": "lěng",
        "translation": "Frio",
        "examples": [
            "今天很冷。 (Jīntiān hěn lěng.) (Hoje está muito frio.)",
            "我觉得冷。 (Wǒ juédé lěng.) (Eu estou com frio.)",
            "请关窗户，很冷。 (Qǐng guān chuānghu, hěn lěng.) (Por favor, feche a janela, está frio.)"
        ]
    },
    {
        "ideogram": "里",
        "pinyin": "lǐ",
        "translation": "Dentro",
        "examples": [
            "在房间里 (Zài fángjiān lǐ) (Dentro do quarto)",
            "书在书包里。 (Shū zài shūbāo lǐ.) (O livro está dentro da mochila.)",
            "我家在城里。 (Wǒ jiā zài chéng lǐ.) (Minha casa fica dentro da cidade.)"
        ]
    },
    {
        "ideogram": "六",
        "pinyin": "liù",
        "translation": "Seis",
        "examples": [
            "六个人 (Liù gè rén) (Seis pessoas)",
            "现在是六点。 (Xiànzài shì liù diǎn.) (Agora são seis horas.)",
            "我买了六本书。 (Wǒ mǎile liù běn shū.) (Eu comprei seis livros.)"
        ]
    },
    {
        "ideogram": "妈妈",
        "pinyin": "mā ma",
        "translation": "Mãe",
        "examples": [
            "我爱妈妈。 (Wǒ ài māma.) (Eu amo a mamãe.)",
            "妈妈在做饭。 (Māma zài zuòfàn.) (Mamãe está cozinhando.)",
            "我妈妈是老师。 (Wǒ māma shì lǎoshī.) (Minha mãe é professora.)"
        ]
    },
    {
        "ideogram": "吗",
        "pinyin": "ma",
        "translation": "Partícula interrogativa",
        "examples": [
            "你好吗？ (Nǐ hǎo ma?) (Como você está?)",
            "这是你的书吗？ (Zhè shì nǐ de shū ma?) (Este é o seu livro?)",
            "你喜欢茶吗？ (Nǐ xǐhuān chá ma?) (Você gosta de chá?)"
        ]
    },
    {
        "ideogram": "买",
        "pinyin": "mǎi",
        "translation": "Comprar",
        "examples": [
            "我买书。 (Wǒ mǎi shū.) (Eu compro livros.)",
            "你买什么？ (Nǐ mǎi shénme?) (O que você está comprando?)",
            "请帮我买一杯咖啡。 (Qǐng bāng wǒ mǎi yī bēi kāfēi.) (Por favor, me compre uma xícara de café.)"
        ]
    },
    {
        "ideogram": "猫",
        "pinyin": "māo",
        "translation": "Gato",
        "examples": [
            "这只猫很可爱。 (Zhè zhī māo hěn kě'ài.) (Este gato é muito fofo.)",
            "我有一只猫。 (Wǒ yǒu yī zhī māo.) (Eu tenho um gato.)",
            "猫在睡觉。 (Māo zài shuìjiào.) (O gato está dormindo.)"
        ]
    },
    {
        "ideogram": "没关系",
        "pinyin": "méi guān xi",
        "translation": "Não tem problema",
        "examples": [
            "没关系！ (Méi guānxi!) (Não tem problema!)",
            "对不起，我迟到了。没关系。 (Duìbuqǐ, wǒ chídào le. Méi guānxi.) (Desculpe, eu me atrasei. Não tem problema.)",
            "没关系，我们可以等。 (Méi guānxi, wǒmen kěyǐ děng.) (Não tem problema, podemos esperar.)"
        ]
    },
    {
        "ideogram": "没有",
        "pinyin": "méi yǒu",
        "translation": "Não ter",
        "examples": [
            "我没有钱。 (Wǒ méiyǒu qián.) (Eu não tenho dinheiro.)",
            "他没有时间。 (Tā méiyǒu shíjiān.) (Ele não tem tempo.)",
            "这里没有人。 (Zhèlǐ méiyǒu rén.) (Não há ninguém aqui.)"
        ]
    },
    {
        "ideogram": "米饭",
        "pinyin": "mǐ fàn",
        "translation": "Arroz cozido",
        "examples": [
            "我吃米饭。 (Wǒ chī mǐfàn.) (Eu como arroz.)",
            "米饭很好吃。 (Mǐfàn hěn hǎo chī.) (O arroz está muito gostoso.)",
            "请给我一碗米饭。 (Qǐng gěi wǒ yī wǎn mǐfàn.) (Por favor, me dê uma tigela de arroz.)"
        ]
    },
    {
        "ideogram": "名字",
        "pinyin": "míng zì",
        "translation": "Nome",
        "examples": [
            "你叫什么名字？ (Nǐ jiào shénme míngzì?) (Qual é o seu nome?)",
            "我的名字是李明。 (Wǒ de míngzì shì Lǐ Míng.) (Meu nome é Li Ming.)",
            "这个名字很好听。 (Zhège míngzì hěn hǎotīng.) (Este nome é muito bonito.)"
        ]
    },
        {
        "ideogram": "明天",
        "pinyin": "míng tiān",
        "translation": "Amanhã",
        "examples": [
            "明天见。 (Míngtiān jiàn.) (Até amanhã.)",
            "明天我们去公园。 (Míngtiān wǒmen qù gōngyuán.) (Amanhã vamos ao parque.)",
            "明天是我的生日。 (Míngtiān shì wǒ de shēngrì.) (Amanhã é o meu aniversário.)"
        ]
    },
    {
        "ideogram": "哪",
        "pinyin": "nǎ",
        "translation": "Qual",
        "examples": [
            "你去哪？ (Nǐ qù nǎ?) (Para onde você vai?)",
            "这是哪本书？ (Zhè shì nǎ běn shū?) (Qual é este livro?)",
            "你喜欢哪种颜色？ (Nǐ xǐhuān nǎ zhǒng yánsè?) (Qual cor você gosta?)"
        ]
    },
    {
        "ideogram": "哪儿",
        "pinyin": "nǎr",
        "translation": "Onde",
        "examples": [
            "你在哪儿？ (Nǐ zài nǎr?) (Onde você está?)",
            "我们去哪儿吃饭？ (Wǒmen qù nǎr chīfàn?) (Onde vamos comer?)",
            "书在哪儿？ (Shū zài nǎr?) (Onde está o livro?)"
        ]
    },
    {
        "ideogram": "那",
        "pinyin": "nà",
        "translation": "Aquilo",
        "examples": [
            "那是谁？ (Nà shì shéi?) (Quem é aquele?)",
            "那是我的书。 (Nà shì wǒ de shū.) (Aquele é o meu livro.)",
            "那家饭店很好吃。 (Nà jiā fàndiàn hěn hǎo chī.) (Aquele restaurante é muito gostoso.)"
        ]
    },
    {
        "ideogram": "呢",
        "pinyin": "ne",
        "translation": "Partícula interrogativa",
        "examples": [
            "你呢？ (Nǐ ne?) (E você?)",
            "我的书呢？ (Wǒ de shū ne?) (Onde está o meu livro?)",
            "他去哪儿呢？ (Tā qù nǎr ne?) (Para onde ele foi?)"
        ]
    },
    {
        "ideogram": "能",
        "pinyin": "néng",
        "translation": "Poder",
        "examples": [
            "我能去吗？ (Wǒ néng qù ma?) (Eu posso ir?)",
            "你能帮我吗？ (Nǐ néng bāng wǒ ma?) (Você pode me ajudar?)",
            "他能说汉语。 (Tā néng shuō Hànyǔ.) (Ele sabe falar chinês.)"
        ]
    },
    {
        "ideogram": "你",
        "pinyin": "nǐ",
        "translation": "Você",
        "examples": [
            "你好！ (Nǐ hǎo!) (Olá!)",
            "你叫什么名字？ (Nǐ jiào shénme míngzì?) (Qual é o seu nome?)",
            "你喜欢什么？ (Nǐ xǐhuān shénme?) (O que você gosta?)"
        ]
    },
    {
        "ideogram": "年",
        "pinyin": "nián",
        "translation": "Ano",
        "examples": [
            "今年是2023年。 (Jīnnián shì 2023 nián.) (Este ano é 2023.)",
            "我去年去了中国。 (Wǒ qùnián qùle Zhōngguó.) (Eu fui para a China no ano passado.)",
            "明年我毕业。 (Míngnián wǒ bìyè.) (Eu me formo no próximo ano.)"
        ]
    },
    {
        "ideogram": "女儿",
        "pinyin": "nǚ ér",
        "translation": "Filha",
        "examples": [
            "我有一个女儿。 (Wǒ yǒu yīgè nǚ'ér.) (Eu tenho uma filha.)",
            "我女儿很聪明。 (Wǒ nǚ'ér hěn cōngmíng.) (Minha filha é muito inteligente.)",
            "他女儿是医生。 (Tā nǚ'ér shì yīshēng.) (A filha dele é médica.)"
        ]
    },
    {
        "ideogram": "朋友",
        "pinyin": "péng you",
        "translation": "Amigo",
        "examples": [
            "他是我的朋友。 (Tā shì wǒ de péngyou.) (Ele é meu amigo.)",
            "我有很多朋友。 (Wǒ yǒu hěn duō péngyou.) (Eu tenho muitos amigos.)",
            "我们一起去看电影吧。 (Wǒmen yīqǐ qù kàn diànyǐng ba.) (Vamos assistir a um filme juntos.)"
        ]
    },
    {
        "ideogram": "漂亮",
        "pinyin": "piào liang",
        "translation": "Bonito",
        "examples": [
            "她很漂亮。 (Tā hěn piàoliang.) (Ela é muito bonita.)",
            "这件衣服很漂亮。 (Zhè jiàn yīfu hěn piàoliang.) (Esta roupa é muito bonita.)",
            "这个花园真漂亮。 (Zhège huāyuán zhēn piàoliang.) (Este jardim é muito bonito.)"
        ]
    },
    {
        "ideogram": "苹果",
        "pinyin": "píng guǒ",
        "translation": "Maçã",
        "examples": [
            "我吃苹果。 (Wǒ chī píngguǒ.) (Eu como maçãs.)",
            "这个苹果很甜。 (Zhège píngguǒ hěn tián.) (Esta maçã é muito doce.)",
            "请给我一个苹果。 (Qǐng gěi wǒ yīgè píngguǒ.) (Por favor, me dê uma maçã.)"
        ]
    },
    {
        "ideogram": "七",
        "pinyin": "qī",
        "translation": "Sete",
        "examples": [
            "七个人 (Qī gè rén) (Sete pessoas)",
            "现在是七点。 (Xiànzài shì qī diǎn.) (Agora são sete horas.)",
            "我买了七本书。 (Wǒ mǎile qī běn shū.) (Eu comprei sete livros.)"
        ]
    },
    {
        "ideogram": "钱",
        "pinyin": "qián",
        "translation": "Dinheiro",
        "examples": [
            "我有钱。 (Wǒ yǒu qián.) (Eu tenho dinheiro.)",
            "这本书多少钱？ (Zhè běn shū duōshǎo qián?) (Quanto custa este livro?)",
            "请给我一些钱。 (Qǐng gěi wǒ yīxiē qián.) (Por favor, me dê um pouco de dinheiro.)"
        ]
    },
    {
        "ideogram": "前面",
        "pinyin": "qián miàn",
        "translation": "Frente",
        "examples": [
            "他在前面。 (Tā zài qiánmiàn.) (Ele está na frente.)",
            "请坐在前面。 (Qǐng zuò zài qiánmiàn.) (Por favor, sente-se na frente.)",
            "房子前面有一个花园。 (Fángzi qiánmiàn yǒu yīgè huāyuán.) (Há um jardim na frente da casa.)"
        ]
    },
    {
        "ideogram": "请",
        "pinyin": "qǐng",
        "translation": "Por favor",
        "examples": [
            "请坐。 (Qǐng zuò.) (Por favor, sente-se.)",
            "请帮我。 (Qǐng bāng wǒ.) (Por favor, me ajude.)",
            "请给我一杯水。 (Qǐng gěi wǒ yī bēi shuǐ.) (Por favor, me dê um copo de água.)"
        ]
    },
    {
        "ideogram": "去",
        "pinyin": "qù",
        "translation": "Ir",
        "examples": [
            "我去学校。 (Wǒ qù xuéxiào.) (Eu vou para a escola.)",
            "你去哪儿？ (Nǐ qù nǎr?) (Para onde você vai?)",
            "我们一起去吧。 (Wǒmen yīqǐ qù ba.) (Vamos juntos.)"
        ]
    },
    {
        "ideogram": "热",
        "pinyin": "rè",
        "translation": "Quente",
        "examples": [
            "今天很热。 (Jīntiān hěn rè.) (Hoje está muito quente.)",
            "这杯茶很热。 (Zhè bēi chá hěn rè.) (Este chá está muito quente.)",
            "请小心，水很热。 (Qǐng xiǎoxīn, shuǐ hěn rè.) (Por favor, cuidado, a água está quente.)"
        ]
    },
    {
        "ideogram": "人",
        "pinyin": "rén",
        "translation": "Pessoa",
        "examples": [
            "很多人 (Hěn duō rén) (Muitas pessoas)",
            "他是一个好人。 (Tā shì yīgè hǎo rén.) (Ele é uma boa pessoa.)",
            "这里没有人。 (Zhèlǐ méiyǒu rén.) (Não há ninguém aqui.)"
        ]
    },
    {
        "ideogram": "认识",
        "pinyin": "rèn shi",
        "translation": "Conhecer",
        "examples": [
            "我认识他。 (Wǒ rènshi tā.) (Eu conheço ele.)",
            "你认识这个地方吗？ (Nǐ rènshi zhège dìfāng ma?) (Você conhece este lugar?)",
            "我们认识很久了。 (Wǒmen rènshi hěn jiǔ le.) (Nós nos conhecemos há muito tempo.)"
        ]
    },
    {
        "ideogram": "日",
        "pinyin": "rì",
        "translation": "Dia",
        "examples": [
            "今天是星期几？ (Jīntiān shì xīngqī jǐ?) (Que dia é hoje?)",
            "我每天学习汉语。 (Wǒ měitiān xuéxí Hànyǔ.) (Eu estudo chinês todos os dias.)",
            "星期日我们休息。 (Xīngqīrì wǒmen xiūxi.) (No domingo nós descansamos.)"
        ]
    },
    {
        "ideogram": "三",
        "pinyin": "sān",
        "translation": "Três",
        "examples": [
            "三个人 (Sān gè rén) (Três pessoas)",
            "现在是三点。 (Xiànzài shì sān diǎn.) (Agora são três horas.)",
            "我买了三本书。 (Wǒ mǎile sān běn shū.) (Eu comprei três livros.)"
        ]
    },
    {
        "ideogram": "商店",
        "pinyin": "shāng diàn",
        "translation": "Loja",
        "examples": [
            "我去商店买东西。 (Wǒ qù shāngdiàn mǎi dōngxi.) (Eu vou à loja comprar coisas.)",
            "这家商店很大。 (Zhè jiā shāngdiàn hěn dà.) (Esta loja é muito grande.)",
            "商店里有很多人。 (Shāngdiàn lǐ yǒu hěn duō rén.) (Há muitas pessoas na loja.)"
        ]
    },
    {
        "ideogram": "上",
        "pinyin": "shàng",
        "translation": "Em cima",
        "examples": [
            "书在桌子上。 (Shū zài zhuōzi shàng.) (O livro está em cima da mesa.)",
            "请上楼。 (Qǐng shàng lóu.) (Por favor, suba as escadas.)",
            "他在上班。 (Tā zài shàngbān.) (Ele está no trabalho.)"
        ]
    },
    {
        "ideogram": "上午",
        "pinyin": "shàng wǔ",
        "translation": "Manhã",
        "examples": [
            "上午好！ (Shàngwǔ hǎo!) (Bom dia!)",
            "我上午学习。 (Wǒ shàngwǔ xuéxí.) (Eu estudo de manhã.)",
            "上午我们去公园。 (Shàngwǔ wǒmen qù gōngyuán.) (De manhã vamos ao parque.)"
        ]
    },
    {
        "ideogram": "少",
        "pinyin": "shǎo",
        "translation": "Pouco",
        "examples": [
            "这里人很少。 (Zhèlǐ rén hěn shǎo.) (Há poucas pessoas aqui.)",
            "请少放糖。 (Qǐng shǎo fàng táng.) (Por favor, coloque pouco açúcar.)",
            "我很少喝咖啡。 (Wǒ hěn shǎo hē kāfēi.) (Eu raramente bebo café.)"
        ]
    },
    {
        "ideogram": "谁",
        "pinyin": "shéi",
        "translation": "Quem",
        "examples": [
            "你是谁？ (Nǐ shì shéi?) (Quem é você?)",
            "这是谁的书？ (Zhè shì shéi de shū?) (De quem é este livro?)",
            "谁来了？ (Shéi lái le?) (Quem chegou?)"
        ]
    },
    {
        "ideogram": "什么",
        "pinyin": "shén me",
        "translation": "O que",
        "examples": [
            "这是什么？ (Zhè shì shénme?) (O que é isso?)",
            "你喜欢什么？ (Nǐ xǐhuān shénme?) (O que você gosta?)",
            "你在做什么？ (Nǐ zài zuò shénme?) (O que você está fazendo?)"
        ]
    },
    {
        "ideogram": "十",
        "pinyin": "shí",
        "translation": "Dez",
        "examples": [
            "十个人 (Shí gè rén) (Dez pessoas)",
            "现在是十点。 (Xiànzài shì shí diǎn.) (Agora são dez horas.)",
            "我买了十本书。 (Wǒ mǎile shí běn shū.) (Eu comprei dez livros.)"
        ]
    },
    {
        "ideogram": "时候",
        "pinyin": "shí hou",
        "translation": "Hora, momento",
        "examples": [
            "现在是什么时候？ (Xiànzài shì shénme shíhòu?) (Que horas são agora?)",
            "你什么时候来？ (Nǐ shénme shíhòu lái?) (Quando você vem?)",
            "我们小时候是朋友。 (Wǒmen xiǎoshíhòu shì péngyou.) (Nós éramos amigos quando éramos crianças.)"
        ]
    },
    {
        "ideogram": "是",
        "pinyin": "shì",
        "translation": "Ser",
        "examples": [
            "我是学生。 (Wǒ shì xuéshēng.) (Eu sou estudante.)",
            "这是你的书吗？ (Zhè shì nǐ de shū ma?) (Este é o seu livro?)",
            "他是我的老师。 (Tā shì wǒ de lǎoshī.) (Ele é meu professor.)"
        ]
    },
    {
        "ideogram": "书",
        "pinyin": "shū",
        "translation": "Livro",
        "examples": [
            "这是我的书。 (Zhè shì wǒ de shū.) (Este é o meu livro.)",
            "我喜欢读书。 (Wǒ xǐhuān dúshū.) (Eu gosto de ler livros.)",
            "请给我一本书。 (Qǐng gěi wǒ yī běn shū.) (Por favor, me dê um livro.)"
        ]
    },
    {
        "ideogram": "水",
        "pinyin": "shuǐ",
        "translation": "Água",
        "examples": [
            "我喝水。 (Wǒ hē shuǐ.) (Eu bebo água.)",
            "请给我一杯水。 (Qǐng gěi wǒ yī bēi shuǐ.) (Por favor, me dê um copo de água.)",
            "水很冷。 (Shuǐ hěn lěng.) (A água está muito fria.)"
        ]
    },
    {
        "ideogram": "水果",
        "pinyin": "shuǐ guǒ",
        "translation": "Fruta",
        "examples": [
            "我喜欢吃水果。 (Wǒ xǐhuān chī shuǐguǒ.) (Eu gosto de comer frutas.)",
            "这个水果很甜。 (Zhège shuǐguǒ hěn tián.) (Esta fruta é muito doce.)",
            "请买一些水果。 (Qǐng mǎi yīxiē shuǐguǒ.) (Por favor, compre algumas frutas.)"
        ]
    },
       {
        "ideogram": "睡觉",
        "pinyin": "shuì jiào",
        "translation": "Dormir",
        "examples": [
            "我去睡觉。 (Wǒ qù shuìjiào.) (Eu vou dormir.)",
            "他正在睡觉。 (Tā zhèngzài shuìjiào.) (Ele está dormindo.)",
            "请安静，孩子在睡觉。 (Qǐng ānjìng, háizi zài shuìjiào.) (Por favor, fique quieto, a criança está dormindo.)"
        ]
    },
    {
        "ideogram": "说",
        "pinyin": "shuō",
        "translation": "Falar",
        "examples": [
            "我说汉语。 (Wǒ shuō Hànyǔ.) (Eu falo chinês.)",
            "请说慢一点。 (Qǐng shuō màn yīdiǎn.) (Por favor, fale mais devagar.)",
            "他说得很好。 (Tā shuō de hěn hǎo.) (Ele fala muito bem.)"
        ]
    },
    {
        "ideogram": "四",
        "pinyin": "sì",
        "translation": "Quatro",
        "examples": [
            "四个人 (Sì gè rén) (Quatro pessoas)",
            "现在是四点。 (Xiànzài shì sì diǎn.) (Agora são quatro horas.)",
            "我买了四本书。 (Wǒ mǎile sì běn shū.) (Eu comprei quatro livros.)"
        ]
    },
    {
        "ideogram": "岁",
        "pinyin": "suì",
        "translation": "Anos de idade",
        "examples": [
            "你几岁？ (Nǐ jǐ suì?) (Quantos anos você tem?)",
            "我二十岁。 (Wǒ èrshí suì.) (Eu tenho vinte anos.)",
            "他儿子五岁。 (Tā érzi wǔ suì.) (O filho dele tem cinco anos.)"
        ]
    },
    {
        "ideogram": "他",
        "pinyin": "tā",
        "translation": "Ele",
        "examples": [
            "他是我的老师。 (Tā shì wǒ de lǎoshī.) (Ele é meu professor.)",
            "他喜欢喝茶。 (Tā xǐhuān hē chá.) (Ele gosta de beber chá.)",
            "他去了北京。 (Tā qùle Běijīng.) (Ele foi para Pequim.)"
        ]
    },
    {
        "ideogram": "她",
        "pinyin": "tā",
        "translation": "Ela",
        "examples": [
            "她是我的朋友。 (Tā shì wǒ de péngyou.) (Ela é minha amiga.)",
            "她喜欢看电影。 (Tā xǐhuān kàn diànyǐng.) (Ela gosta de assistir filmes.)",
            "她去了商店。 (Tā qùle shāngdiàn.) (Ela foi para a loja.)"
        ]
    },
    {
        "ideogram": "太",
        "pinyin": "tài",
        "translation": "Muito",
        "examples": [
            "太好了！ (Tài hǎo le!) (Muito bom!)",
            "今天太热了。 (Jīntiān tài rè le.) (Hoje está muito quente.)",
            "这本书太贵了。 (Zhè běn shū tài guì le.) (Este livro é muito caro.)"
        ]
    },
    {
        "ideogram": "天气",
        "pinyin": "tiān qì",
        "translation": "Clima",
        "examples": [
            "今天天气很好。 (Jīntiān tiānqì hěn hǎo.) (O tempo está muito bom hoje.)",
            "明天的天气怎么样？ (Míngtiān de tiānqì zěnmeyàng?) (Como estará o tempo amanhã?)",
            "天气太冷了。 (Tiānqì tài lěng le.) (O tempo está muito frio.)"
        ]
    },
    {
        "ideogram": "听",
        "pinyin": "tīng",
        "translation": "Ouvir",
        "examples": [
            "我听音乐。 (Wǒ tīng yīnyuè.) (Eu ouço música.)",
            "请听我说。 (Qǐng tīng wǒ shuō.) (Por favor, me escute.)",
            "他听不清楚。 (Tā tīng bù qīngchǔ.) (Ele não consegue ouvir claramente.)"
        ]
    },
    {
        "ideogram": "同学",
        "pinyin": "tóng xué",
        "translation": "Colega de classe",
        "examples": [
            "他是我的同学。 (Tā shì wǒ de tóngxué.) (Ele é meu colega de classe.)",
            "我们一起学习。 (Wǒmen yīqǐ xuéxí.) (Nós estudamos juntos.)",
            "我的同学很聪明。 (Wǒ de tóngxué hěn cōngmíng.) (Meu colega de classe é muito inteligente.)"
        ]
    },
    {
        "ideogram": "喂",
        "pinyin": "wèi",
        "translation": "Alô",
        "examples": [
            "喂，你好！ (Wèi, nǐ hǎo!) (Alô, olá!)",
            "喂，请问是谁？ (Wèi, qǐng wèn shì shéi?) (Alô, quem está falando?)",
            "喂，我听不清楚。 (Wèi, wǒ tīng bù qīngchǔ.) (Alô, não consigo ouvir bem.)"
        ]
    },
    {
        "ideogram": "我",
        "pinyin": "wǒ",
        "translation": "Eu",
        "examples": [
            "我是学生。 (Wǒ shì xuéshēng.) (Eu sou estudante.)",
            "我喜欢喝茶。 (Wǒ xǐhuān hē chá.) (Eu gosto de beber chá.)",
            "我去学校。 (Wǒ qù xuéxiào.) (Eu vou para a escola.)"
        ]
    },
    {
        "ideogram": "我们",
        "pinyin": "wǒ men",
        "translation": "Nós",
        "examples": [
            "我们去学校。 (Wǒmen qù xuéxiào.) (Nós vamos para a escola.)",
            "我们一起学习。 (Wǒmen yīqǐ xuéxí.) (Nós estudamos juntos.)",
            "我们的老师很好。 (Wǒmen de lǎoshī hěn hǎo.) (Nosso professor é muito bom.)"
        ]
    },
    {
        "ideogram": "五",
        "pinyin": "wǔ",
        "translation": "Cinco",
        "examples": [
            "五个人 (Wǔ gè rén) (Cinco pessoas)",
            "现在是五点。 (Xiànzài shì wǔ diǎn.) (Agora são cinco horas.)",
            "我买了五本书。 (Wǒ mǎile wǔ běn shū.) (Eu comprei cinco livros.)"
        ]
    },
    {
        "ideogram": "喜欢",
        "pinyin": "xǐ huān",
        "translation": "Gostar",
        "examples": [
            "我喜欢你。 (Wǒ xǐhuān nǐ.) (Eu gosto de você.)",
            "他喜欢喝茶。 (Tā xǐhuān hē chá.) (Ele gosta de beber chá.)",
            "你喜欢什么颜色？ (Nǐ xǐhuān shénme yánsè?) (De que cor você gosta?)"
        ]
    },
    {
        "ideogram": "下",
        "pinyin": "xià",
        "translation": "Embaixo",
        "examples": [
            "书在桌子下。 (Shū zài zhuōzi xià.) (O livro está embaixo da mesa.)",
            "请下楼。 (Qǐng xià lóu.) (Por favor, desça as escadas.)",
            "他在下班。 (Tā zài xiàbān.) (Ele está saindo do trabalho.)"
        ]
    },
    {
        "ideogram": "下午",
        "pinyin": "xià wǔ",
        "translation": "Tarde",
        "examples": [
            "下午好！ (Xiàwǔ hǎo!) (Boa tarde!)",
            "我下午学习。 (Wǒ xiàwǔ xuéxí.) (Eu estudo à tarde.)",
            "下午我们去公园。 (Xiàwǔ wǒmen qù gōngyuán.) (À tarde vamos ao parque.)"
        ]
    },
    {
        "ideogram": "下雨",
        "pinyin": "xià yǔ",
        "translation": "Chover",
        "examples": [
            "今天下雨。 (Jīntiān xià yǔ.) (Hoje está chovendo.)",
            "下雨了，带伞吧。 (Xià yǔ le, dài sǎn ba.) (Está chovendo, leve um guarda-chuva.)",
            "昨天下午下雨了。 (Zuótiān xiàwǔ xià yǔ le.) (Choveu ontem à tarde.)"
        ]
    },
    {
        "ideogram": "先生",
        "pinyin": "xiān sheng",
        "translation": "Senhor",
        "examples": [
            "你好，先生！ (Nǐ hǎo, xiānsheng!) (Olá, senhor!)",
            "这位先生是谁？ (Zhè wèi xiānsheng shì shéi?) (Quem é este senhor?)",
            "先生，请坐。 (Xiānsheng, qǐng zuò.) (Senhor, por favor, sente-se.)"
        ]
    },
    {
        "ideogram": "现在",
        "pinyin": "xiàn zài",
        "translation": "Agora",
        "examples": [
            "现在几点？ (Xiànzài jǐ diǎn?) (Que horas são agora?)",
            "我现在很忙。 (Wǒ xiànzài hěn máng.) (Eu estou muito ocupado agora.)",
            "现在我们去吃饭吧。 (Xiànzài wǒmen qù chīfàn ba.) (Agora vamos comer.)"
        ]
    },
    {
        "ideogram": "想",
        "pinyin": "xiǎng",
        "translation": "Pensar, querer",
        "examples": [
            "我想去中国。 (Wǒ xiǎng qù Zhōngguó.) (Eu quero ir para a China.)",
            "你在想什么？ (Nǐ zài xiǎng shénme?) (No que você está pensando?)",
            "我想喝咖啡。 (Wǒ xiǎng hē kāfēi.) (Eu quero beber café.)"
        ]
    },
    {
        "ideogram": "小",
        "pinyin": "xiǎo",
        "translation": "Pequeno",
        "examples": [
            "这个房子很小。 (Zhège fángzi hěn xiǎo.) (Esta casa é muito pequena.)",
            "我有一只小狗。 (Wǒ yǒu yī zhī xiǎo gǒu.) (Eu tenho um cachorrinho.)",
            "请给我一个小杯子。 (Qǐng gěi wǒ yīgè xiǎo bēizi.) (Por favor, me dê um copo pequeno.)"
        ]
    },
    {
        "ideogram": "小姐",
        "pinyin": "xiǎo jiě",
        "translation": "Senhorita",
        "examples": [
            "你好，小姐！ (Nǐ hǎo, xiǎojiě!) (Olá, senhorita!)",
            "这位小姐是谁？ (Zhè wèi xiǎojiě shì shéi?) (Quem é esta senhorita?)",
            "小姐，请帮我。 (Xiǎojiě, qǐng bāng wǒ.) (Senhorita, por favor, me ajude.)"
        ]
    },
    {
        "ideogram": "些",
        "pinyin": "xiē",
        "translation": "Alguns",
        "examples": [
            "我买些水果。 (Wǒ mǎi xiē shuǐguǒ.) (Eu compro algumas frutas.)",
            "请给我一些水。 (Qǐng gěi wǒ yīxiē shuǐ.) (Por favor, me dê um pouco de água.)",
            "这些书很好。 (Zhèxiē shū hěn hǎo.) (Estes livros são muito bons.)"
        ]
    },
    {
        "ideogram": "写",
        "pinyin": "xiě",
        "translation": "Escrever",
        "examples": [
            "我写信。 (Wǒ xiě xìn.) (Eu escrevo uma carta.)",
            "请写你的名字。 (Qǐng xiě nǐ de míngzì.) (Por favor, escreva seu nome.)",
            "他写得很好。 (Tā xiě de hěn hǎo.) (Ele escreve muito bem.)"
        ]
    },
    {
        "ideogram": "谢谢",
        "pinyin": "xiè xie",
        "translation": "Obrigado",
        "examples": [
            "谢谢！ (Xièxie!) (Obrigado!)",
            "谢谢你的帮助。 (Xièxie nǐ de bāngzhù.) (Obrigado pela sua ajuda.)",
            "不客气，谢谢！ (Bù kèqi, xièxie!) (De nada, obrigado!)"
        ]
    },
    {
        "ideogram": "星期",
        "pinyin": "xīng qī",
        "translation": "Semana",
        "examples": [
            "今天是星期几？ (Jīntiān shì xīngqī jǐ?) (Que dia é hoje?)",
            "星期一我去工作。 (Xīngqīyī wǒ qù gōngzuò.) (Na segunda-feira eu vou trabalhar.)",
            "星期天我们休息。 (Xīngqītiān wǒmen xiūxi.) (No domingo nós descansamos.)"
        ]
    },
    {
        "ideogram": "学生",
        "pinyin": "xué sheng",
        "translation": "Estudante",
        "examples": [
            "我是学生。 (Wǒ shì xuéshēng.) (Eu sou estudante.)",
            "他是我的学生。 (Tā shì wǒ de xuéshēng.) (Ele é meu aluno.)",
            "学生们在教室里。 (Xuéshēngmen zài jiàoshì lǐ.) (Os alunos estão na sala de aula.)"
        ]
    },
    {
        "ideogram": "学习",
        "pinyin": "xué xí",
        "translation": "Estudar",
        "examples": [
            "我学习汉语。 (Wǒ xuéxí Hànyǔ.) (Eu estudo chinês.)",
            "他学习很努力。 (Tā xuéxí hěn nǔlì.) (Ele estuda muito.)",
            "我们一起学习吧。 (Wǒmen yīqǐ xuéxí ba.) (Vamos estudar juntos.)"
        ]
    },
    {
        "ideogram": "学校",
        "pinyin": "xué xiào",
        "translation": "Escola",
        "examples": [
            "我去学校。 (Wǒ qù xuéxiào.) (Eu vou para a escola.)",
            "这是我们的学校。 (Zhè shì wǒmen de xuéxiào.) (Esta é a nossa escola.)",
            "学校很大。 (Xuéxiào hěn dà.) (A escola é muito grande.)"
        ]
    },
    {
        "ideogram": "一",
        "pinyin": "yī",
        "translation": "Um",
        "examples": [
            "一个人 (Yī gè rén) (Uma pessoa)",
            "我有一本书。 (Wǒ yǒu yī běn shū.) (Eu tenho um livro.)",
            "请给我一杯水。 (Qǐng gěi wǒ yī bēi shuǐ.) (Por favor, me dê um copo de água.)"
        ]
    },
    {
        "ideogram": "衣服",
        "pinyin": "yī fu",
        "translation": "Roupa",
        "examples": [
            "我买衣服。 (Wǒ mǎi yīfu.) (Eu compro roupas.)",
            "这件衣服很漂亮。 (Zhè jiàn yīfu hěn piàoliang.) (Esta roupa é muito bonita.)",
            "请洗这些衣服。 (Qǐng xǐ zhèxiē yīfu.) (Por favor, lave estas roupas.)"
        ]
    },
    {
        "ideogram": "医生",
        "pinyin": "yī shēng",
        "translation": "Médico",
        "examples": [
            "他是医生。 (Tā shì yīshēng.) (Ele é médico.)",
            "我去看医生。 (Wǒ qù kàn yīshēng.) (Eu vou ao médico.)",
            "医生很忙。 (Yīshēng hěn máng.) (O médico está muito ocupado.)"
        ]
    },
{
    "ideogram": "椅子",
    "pinyin": "yǐ zi",
    "translation": "Cadeira",
    "examples": [
        "这是一把椅子。 (Zhè shì yī bǎ yǐzi.) (Esta é uma cadeira.)",
        "椅子很舒服。 (Yǐzi hěn shūfu.) (A cadeira é muito confortável.)",
        "我买了一把椅子。 (Wǒ mǎile yī bǎ yǐzi.) (Eu comprei uma cadeira.)"
    ]
},
{
    "ideogram": "有",
    "pinyin": "yǒu",
    "translation": "Ter",
    "examples": [
        "我有钱。 (Wǒ yǒu qián.) (Eu tenho dinheiro.)",
        "你有时间吗？ (Nǐ yǒu shíjiān ma?) (Você tem tempo?)",
        "他有一本书。 (Tā yǒu yī běn shū.) (Ele tem um livro.)"
    ]
},
{
    "ideogram": "月",
    "pinyin": "yuè",
    "translation": "Mês",
    "examples": [
        "这个月是几月？ (Zhège yuè shì jǐ yuè?) (Que mês é este?)",
        "每个月都有新计划。 (Měi gè yuè dōu yǒu xīn jìhuà.) (Todo mês tem novos planos.)",
        "下个月是我的生日。 (Xià gè yuè shì wǒ de shēngrì.) (Mês que vem é meu aniversário.)"
    ]
},
{
    "ideogram": "在",
    "pinyin": "zài",
    "translation": "Estar",
    "examples": [
        "我在家。 (Wǒ zài jiā.) (Eu estou em casa.)",
        "他在学校。 (Tā zài xuéxiào.) (Ele está na escola.)",
        "书在桌子上。 (Shū zài zhuōzi shàng.) (O livro está na mesa.)"
    ]
},
{
    "ideogram": "再见",
    "pinyin": "zài jiàn",
    "translation": "Tchau",
    "examples": [
        "再见！ (Zàijiàn!) (Tchau!)",
        "明天见，再见！ (Míngtiān jiàn, zàijiàn!) (Até amanhã, tchau!)",
        "他说了再见就走了。 (Tā shuōle zàijiàn jiù zǒule.) (Ele disse tchau e foi embora.)"
    ]
},
{
    "ideogram": "怎么",
    "pinyin": "zěn me",
    "translation": "Como",
    "examples": [
        "你怎么去？ (Nǐ zěnme qù?) (Como você vai?)",
        "这个字怎么写？ (Zhège zì zěnme xiě?) (Como se escreve este caractere?)",
        "我不知道怎么说。 (Wǒ bù zhīdào zěnme shuō.) (Eu não sei como dizer.)"
    ]
},
{
    "ideogram": "怎么样",
    "pinyin": "zěn me yàng",
    "translation": "Como está",
    "examples": [
        "你怎么样？ (Nǐ zěnmeyàng?) (Como você está?)",
        "天气怎么样？ (Tiānqì zěnmeyàng?) (Como está o tempo?)",
        "这本书怎么样？ (Zhè běn shū zěnmeyàng?) (O que acha deste livro?)"
    ]
},
{
    "ideogram": "这",
    "pinyin": "zhè",
    "translation": "Este",
    "examples": [
        "这是谁？ (Zhè shì shéi?) (Quem é este?)",
        "这个地方很漂亮。 (Zhège dìfāng hěn piàoliang.) (Este lugar é muito bonito.)",
        "这是我的书。 (Zhè shì wǒ de shū.) (Este é meu livro.)"
    ]
},
{
    "ideogram": "中国",
    "pinyin": "Zhōng guó",
    "translation": "China",
    "examples": [
        "我去中国。 (Wǒ qù Zhōngguó.) (Eu vou para a China.)",
        "中国很大。 (Zhōngguó hěn dà.) (A China é muito grande.)",
        "中国文化很有趣。 (Zhōngguó wénhuà hěn yǒuqù.) (A cultura chinesa é muito interessante.)"
    ]
},
{
    "ideogram": "中午",
    "pinyin": "zhōng wǔ",
    "translation": "Meio-dia",
    "examples": [
        "中午好！ (Zhōngwǔ hǎo!) (Boa tarde!)",
        "我们中午吃饭。 (Wǒmen zhōngwǔ chīfàn.) (Nós almoçamos ao meio-dia.)",
        "中午的时候太阳很大。 (Zhōngwǔ de shíhòu tàiyáng hěn dà.) (Ao meio-dia o sol está muito forte.)"
    ]
},
{
    "ideogram": "住",
    "pinyin": "zhù",
    "translation": "Morar",
    "examples": [
        "我住在北京。 (Wǒ zhù zài Běijīng.) (Eu moro em Pequim.)",
        "他们住在一栋大房子里。 (Tāmen zhù zài yī dòng dà fángzi lǐ.) (Eles moram em uma casa grande.)",
        "你住在哪里？ (Nǐ zhù zài nǎlǐ?) (Onde você mora?)"
    ]
},
{
    "ideogram": "桌子",
    "pinyin": "zhuō zi",
    "translation": "Mesa",
    "examples": [
        "书在桌子上。 (Shū zài zhuōzi shàng.) (O livro está em cima da mesa.)",
        "桌子很重。 (Zhuōzi hěn zhòng.) (A mesa é muito pesada.)",
        "请把杯子放在桌子上。 (Qǐng bǎ bēizi fàng zài zhuōzi shàng.) (Por favor, coloque o copo na mesa.)"
    ]
},
{
    "ideogram": "字",
    "pinyin": "zì",
    "translation": "Caractere",
    "examples": [
        "这是一个汉字。 (Zhè shì yīgè Hànzì.) (Este é um caractere chinês.)",
        "这个字是什么意思？ (Zhège zì shì shénme yìsi?) (O que significa este caractere?)",
        "他的字写得很好。 (Tā de zì xiě de hěn hǎo.) (A caligrafia dele é muito boa.)"
    ]
},
{
    "ideogram": "昨天",
    "pinyin": "zuó tiān",
    "translation": "Ontem",
    "examples": [
        "昨天我去了学校。 (Zuótiān wǒ qùle xuéxiào.) (Ontem eu fui para a escola.)",
        "昨天是星期几？ (Zuótiān shì xīngqī jǐ?) (Que dia da semana foi ontem?)",
        "昨天的天气很好。 (Zuótiān de tiānqì hěn hǎo.) (O tempo estava ótimo ontem.)"
    ]
}

              
    
]



# Função para gerar áudio de uma palavra específica
def generate_audio(word, example, example_index):
    # Verifica se o áudio da palavra já foi gerado
    if not os.path.exists(f"{word['ideogram']}_word.mp3"):
        # Áudio da palavra (repetir 3 vezes)
        tts_word = gTTS(text=word["ideogram"], lang='zh-cn')
        tts_word.save(f"{word['ideogram']}_word.mp3")

    # Gera áudio do exemplo (apenas em chinês)
    example_chinese = example.split(" (")[0]  # Pega apenas a parte em chinês
    example_audio_file = f"{word['ideogram']}_example_{example_index}.mp3"  # Usa o índice do exemplo no nome do arquivo
    if not os.path.exists(example_audio_file):
        tts_example = gTTS(text=example_chinese, lang='zh-cn')
        tts_example.save(example_audio_file)

# Função para reproduzir áudio
def play_audio(audio_file, repeat=1):
    for _ in range(repeat):
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():  # Esperar o áudio terminar
            time.sleep(0.1)

# Função para mostrar o próximo flashcard
def next_flashcard():
    global current_word, current_example_index
    current_example_index = (current_example_index + 1) % len(words[current_word]["examples"])
    if current_example_index == 0:  # Se voltou ao começo, avança para a próxima palavra
        current_word = (current_word + 1) % len(words)
    show_flashcard()

# Função para destacar o ideograma na frase
def highlight_ideogram_in_example(example, ideogram):
    # Encontrar a posição do ideograma na frase
    start = example.find(ideogram)
    if start == -1:
        return example  # Se não encontrar, retorna a frase original

    # Destacar o ideograma na frase
    end = start + len(ideogram)
    highlighted_example = (
        example[:start] +
        f"**{example[start:end]}**" +  # Usamos ** para marcar o texto a ser destacado
        example[end:]
    )
    return highlighted_example

# Função para mostrar o flashcard atual
def show_flashcard():
    word = words[current_word]
    example = word["examples"][current_example_index]  # Seleciona o exemplo atual

    # Gerar áudio da palavra e do exemplo (se ainda não existirem)
    generate_audio(word, example, current_example_index)

    # Exibir o ideograma, pinyin e tradução
    ideogram_label.config(text=word["ideogram"], fg="blue", font=("Arial", 48, "bold"))
    pinyin_label.config(text=word["pinyin"], font=("Arial", 24))
    translation_label.config(text=word["translation"], font=("Arial", 18))

    # Separar a frase em chinês, pinyin e tradução
    example_parts = example.split(" (")
    example_chinese = example_parts[0]  # Frase em chinês
    example_pinyin = example_parts[1].rstrip(")")  # Pinyin
    example_translation = example_parts[2].rstrip(")")  # Tradução

    # Destacar o ideograma na frase em chinês
    highlighted_example = highlight_ideogram_in_example(example_chinese, word["ideogram"])

    # Limpar o widget de texto antes de inserir novo conteúdo
    example_text.delete(1.0, tk.END)

    # Inserir a frase em chinês com destaque no ideograma
    start_highlight = example_chinese.find(word["ideogram"])
    end_highlight = start_highlight + len(word["ideogram"])

    example_text.insert(tk.END, example_chinese[:start_highlight])
    example_text.insert(tk.END, example_chinese[start_highlight:end_highlight], "highlight")
    example_text.insert(tk.END, example_chinese[end_highlight:] + "\n")

    # Inserir pinyin e tradução
    example_text.insert(tk.END, f"{example_pinyin}\n{example_translation}")

    # Reproduzir áudio da palavra 3 vezes
    play_audio(f"{word['ideogram']}_word.mp3", repeat=3)

    # Reproduzir áudio do exemplo 1 vez (apenas em chinês)
    example_audio_file = f"{word['ideogram']}_example_{current_example_index}.mp3"
    play_audio(example_audio_file, repeat=1)

    # Alternar a cada 10 segundos
    root.after(10000, next_flashcard)

# Interface gráfica
root = tk.Tk()
root.title("Flashcards HSK 1")
root.geometry("600x500")

# Labels para exibir o flashcard
ideogram_label = tk.Label(root, font=("Arial", 48))
ideogram_label.pack(pady=10)

pinyin_label = tk.Label(root, font=("Arial", 24))
pinyin_label.pack(pady=5)

translation_label = tk.Label(root, font=("Arial", 18))
translation_label.pack(pady=5)

# Widget de texto para exibir a frase de exemplo com destaque
example_text = tk.Text(root, font=("Arial", 14), wrap=tk.WORD, height=5, width=50)
example_text.pack(pady=10)

# Configurar a tag "highlight" para destacar o ideograma
example_text.tag_configure("highlight", foreground="blue", font=("Arial", 14, "bold"))

# Inicializar variáveis
current_word = 0
current_example_index = 0

# Mostrar o primeiro flashcard
show_flashcard()

# Iniciar o loop da interface
root.mainloop()