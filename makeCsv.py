from binance import Client
import csv

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
week27="2 jul 2022"
week28="9 jul 2022"
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



client = Client(None,None)

coin='BTCUSDT'
periyot=Client.KLINE_INTERVAL_1HOUR
start=week37
end=week38


def veriGetir(coin,periyot,start,end):
    mumlar = client.get_historical_klines(coin,periyot,start,end,klines_type=HistoricalKlinesType.FUTURES)
    return mumlar


def csvOlustur(sembol,mumlar):
    csvDosya = open(sembol+'.csv','w',newline='')
    yazici = csv.writer(csvDosya,delimiter=',')
    for mumVerileri in mumlar:
        yazici.writerow(mumVerileri)
    csvDosya.close()

csvOlustur(coin,veriGetir(coin,periyot,start,end))