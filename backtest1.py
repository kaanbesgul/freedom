import pandas as pd
import pandas_ta as ta
from binance import Client
import csv
import time
from binance.enums import HistoricalKlinesType



weeks=["1 Jan 2022","19 Jul 2023"]d


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