import pandas as pd
import pandas_ta as ta
from binance import Client
import csv
import time
from binance.enums import HistoricalKlinesType

week1="1 Jan 2022"
week2="8 Jan 2022"
week3="15 Jan 2022"
week4="22 Jan 2022"
week5="29 Jan 2022"
week6="5 Feb 2022"
week7="12 Feb 2022"
week8="19 Feb 2022"
week9="26 Feb 2022"
week10="5 Mar 2022"
week11="12 Mar 2022"
week12="19 Mar 2022"
week13="26 Mar 2022"
week14="2 Apr 2022"
week15="9 Apr 2022"
week16="16 Apr 2022"
week17="23 Apr 2022"
week18="30 Apr 2022"
week19="7 May 2022"
week20="14 May 2022"
week21="21 May 2022"
week22="28 May 2022"
week23="4 jun 2022"
week24="11 jun 2022"
week25="18 jun 2022"
week26="25 jun 2022"
week27="02 jul 2022"
week28="09 jul 2022"
week29="16 jul 2022"
week30="23 jul 2022"
week31="30 jul 2022"
week32="06 Aug 2022"
week33="13 Aug 2022"
week34="20 Aug 2022"
week35="27 Aug 2022"
week36="03 Sep 2022"
week37="10 Sep 2022"
week38="17 Sep 2022"
week39="24 Sep 2022"
week40="01 Oct 2022"
week41="08 Oct 2022"
week42="15 Oct 2022"
week43="22 Oct 2022"
week44="29 Oct 2022"
week45="05 Nov 2022"
week46="12 Nov 2022"
week47="19 Nov 2022"
week48="26 Nov 2022"
week49="03 Dec 2022"
week50="10 Dec 2022"
week51="17 Dec 2022"
week52="24 Dec 2022"
week53="31 Dec 2022"



weeks=[week1,week2,week3,week4,week5,week6,week7,week8,week9,week10,week11,week12,week13,week14,week15,week16,week17,week18,week19,week20,week21,week22,week23,week24,week25,week26,week27,week28,week29,week30,week31,week32,week33,week34,week35,week36,week37,week38,week39,week40,week41,week42,week43,week44,week45,week46,week47,week48,week49,week50,week51,week52,week53]


client = Client(None,None)

coin='BTCUSDT'
periyot=Client.KLINE_INTERVAL_1HOUR



def veriGetir(coin,periyot,start,end):
    mumlar = client.get_historical_klines(coin,periyot,start,end,klines_type=HistoricalKlinesType.FUTURES)
    return mumlar


def csvOlustur(sembol,mumlar):
    csvDosya = open(sembol+'.csv','w',newline='')
    yazici = csv.writer(csvDosya,delimiter=',')
    for mumVerileri in mumlar:
        yazici.writerow(mumVerileri)
    csvDosya.close()


"""-------------------------------------------------------------------------------------------------------------------------------"""

karliislemsayisi = 0
zararliislemsayisi = 0
baslangicparasi = 100
sonpara = baslangicparasi

def kandela(okunacak_csv):

    global karliislemsayisi,zararliislemsayisi,baslangicparasi,sonpara

    toplamislemsayisi=0
    komisyonorani=108/1000000
    toplamkomisyon=0
    kaldiracorani=20
    karorani=0.6
    zarardurdur=0.3



    basliklar = ["open-time","open","high","low","close","vol","close_time","qav","not","tbbav","tbqav","ignore"]
    df=pd.read_csv(okunacak_csv,names=basliklar)

    sma = ta.sma(df['close'], 50)

    time=pd.to_datetime(df['open-time'], unit="ms")
    open=df['open']
    close=df['close']
    high=df['high']
    low=df['low']
    islemturu="yok"

    for i in range(len(close)):
        if pd.isna(sma[i]) is False:
            if (close[i-3] < sma[i-3] and close[i-2] < sma[i-2] and close[i-1] < sma[i-1] and high[i] >= sma[i]) and islemturu == "yok":
                #Short işlem açma

                isleme_giris_fiyati=sma[i]

                islemden_karla_cikis=isleme_giris_fiyati-(isleme_giris_fiyati*karorani/100)
                islemden_zararla_cikis=isleme_giris_fiyati+(isleme_giris_fiyati*zarardurdur/100)
                islemturu="short"

                #print(f"short işlem açılmıştır zamanı={time[i]},işleme giriş fiyatı={isleme_giris_fiyati}")

                if high[i] >= islemden_zararla_cikis:
                    komisyon = komisyonorani * (sonpara * kaldiracorani)
                    toplamkomisyon += komisyon

                    sonpara = sonpara - (sonpara * kaldiracorani * zarardurdur / 100) - komisyon
                    toplamislemsayisi += 1

                    zararliislemsayisi += 1

                    #print(f"Başarısız,işlem zamanı={time[i]},işlem türü = Short ,sonpara = {sonpara}, işlemden çıkış fiyatı = {islemden_karla_cikis}")

                    islemturu = "yok"

            elif (close[i-3] > sma[i-3] and close[i-2] > sma[i-2] and close[i-1] > sma[i-1] and low[i] <= sma[i]) and islemturu == "yok":
                #Long işlem açma
                isleme_giris_fiyati = sma[i]

                islemden_karla_cikis = isleme_giris_fiyati + (isleme_giris_fiyati * karorani/100)
                islemden_zararla_cikis = isleme_giris_fiyati - (isleme_giris_fiyati * zarardurdur/100)

                islemturu="long"

                #print(f"long işlem açılmıştır zamanı={time[i]},işleme giriş fiyatı={isleme_giris_fiyati}")
                if low[i] <= islemden_zararla_cikis:
                    # islemden zararla çıkma

                    komisyon = komisyonorani * (sonpara * kaldiracorani)
                    toplamkomisyon += komisyon

                    sonpara = sonpara - (sonpara * kaldiracorani * zarardurdur / 100) - komisyon
                    toplamislemsayisi += 1
                    zararliislemsayisi += 1

                    islemturu = "yok"

                    #print(f"Başarısız,işlem zamanı={time[i]},İşlem türü = Long,sonpara = {sonpara},işlemden çıkış fiyatı = {islemden_zararla_cikis}")

            elif islemturu == "short":
                if low[i] <= islemden_karla_cikis:

                    komisyon=komisyonorani*(sonpara*kaldiracorani)
                    toplamkomisyon+=komisyon

                    sonpara=sonpara+(sonpara*kaldiracorani*karorani/100)-komisyon
                    toplamislemsayisi+=1

                    karliislemsayisi+=1

                    #print(f"Başarılı,işlem zamanı={time[i]},işlem türü = Short ,sonpara = {sonpara}, işlemden çıkış fiyatı = {islemden_karla_cikis}")

                    islemturu="yok"
                elif high[i] >= islemden_zararla_cikis:
                    #islemden zararla çıkma

                    komisyon = komisyonorani * (sonpara * kaldiracorani)
                    toplamkomisyon += komisyon

                    sonpara = sonpara - (sonpara * kaldiracorani * zarardurdur / 100)-komisyon
                    toplamislemsayisi += 1
                    zararliislemsayisi += 1
                    islemturu="yok"

                    #print(f"Başarısız,işlem zamanı={time[i]},işlem türü = Short,sonpara = {sonpara}, işlemden çıkış fiyatı = {islemden_zararla_cikis}")
                else:
                    continue

            elif islemturu == "long":
                if high[i] >= islemden_karla_cikis:

                    komisyon = komisyonorani * (sonpara * kaldiracorani)
                    toplamkomisyon += komisyon

                    sonpara = sonpara + (sonpara * kaldiracorani * karorani / 100)-komisyon
                    toplamislemsayisi += 1
                    karliislemsayisi += 1

                    islemturu="yok"

                    #print(f"Başarılı,işlem zamanı={time[i]},işlem türü = Long,sonpara = {sonpara},işlemden çıkış fiyatı = {islemden_karla_cikis}")
                elif low[i] <= islemden_zararla_cikis:
                    #islemden zararla çıkma

                    komisyon = komisyonorani * (sonpara * kaldiracorani)
                    toplamkomisyon += komisyon

                    sonpara = sonpara - (sonpara * kaldiracorani * zarardurdur / 100)-komisyon
                    toplamislemsayisi += 1
                    zararliislemsayisi +=1

                    islemturu="yok"

                    #print(f"Başarısız,işlem zamanı={time[i]},İşlem türü = Long,sonpara = {sonpara},işlemden çıkış fiyatı = {islemden_zararla_cikis}")
                else:
                    continue

            else:

                continue
    print(f"ilkpara={baslangicparasi},sonpara={sonpara},karlıişlem sayısı={karliislemsayisi},zararlı işlem sayısı = {zararliislemsayisi},toplam komisyon={toplamkomisyon}")


for i in range(len(weeks)):
    try:
        start = weeks[i]
        end = weeks[i + 1]
        csvOlustur(coin, veriGetir(coin, periyot, start, end))
        time.sleep(5)
        kandela("BTCUSDT.csv")
    except IndexError:
        print("End of the loop.")