#df_store.isnull().sum()
#
#df_store[pd.isnull(df_store.CompetitionDistance)]
#
## Fehlende Werte der "CompetitionDistance" mit dem Median ersetzen
#df_store['CompetitionDistance'].fillna(df_store['CompetitionDistance'].median(), inplace=True)
#
## Prüfen, ob es CompetitionOpenSince[Month/Year] zusammenhänge gibt, bei denen CompetitionOpenSince[Month/Year] NULL ist
#df_CompetitionOpenSinceMonth = df_store[pd.isnull(df_store.CompetitionOpenSinceMonth)]
#df_CompetitionOpenSinceMonth.head()
#
#print('Month', df_store['CompetitionOpenSinceMonth'].median())
#print('Year', df_store['CompetitionOpenSinceYear'].median())
#df_store['CompetitionOpenSinceYear'].describe()
#
## Es scheint keine Zusammenhänge mit den anderen Werten zu geben, da NULLs aber entfernt werden müssen, werden die Daten mit 0 ersetzt
#df_store['CompetitionOpenSinceMonth'].fillna(0, inplace=True)
#df_store['CompetitionOpenSinceYear'].fillna(0, inplace=True)
#
## Promo2 Zusatzfelder
#Promo2 - Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
#Promo2Since[Year/Week] - describes the year and calendar week when the store started participating in Promo2
#PromoInterval - describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store
#
## Prüfen, ob es zusammenhänge gibt, bei denen die Promo2 Zusatzfelder NULL sind
#df_Promo2SinceWeek = df_store[pd.isnull(df_store.Promo2SinceWeek)]
#df_Promo2SinceWeek.head()
#
## Es sieht so aus, als wären die Felder NULL wenn Promo2 = 0 ist
## Prüfen, ob Promo2SinceWeek, Promo2SinceYear, PromoInterval nur NULL sind, wenn Promo2 auch 0 ist (also der Store an keiner Promo teilnimmt)
#df_Promo2SinceWeek = df_store[pd.isnull(df_store.Promo2SinceWeek)]
#print(df_Promo2SinceWeek[df_Promo2SinceWeek.Promo2 != 0].shape[0])
#
#df_Promo2SinceYear = df_store[pd.isnull(df_store.Promo2SinceYear)]
#print(df_Promo2SinceYear[df_Promo2SinceYear.Promo2 != 0].shape[0])
#
#df_PromoInterval = df_store[pd.isnull(df_store.PromoInterval)]
#print(df_PromoInterval[df_PromoInterval.Promo2 != 0].shape[0])
#
## Ja, NULL in den 3 Spalten bedeutet, dass es keine Information über eine Promo gibt
## Ersetzen der NULL Werte durch 0
#df_store['Promo2SinceWeek'].fillna(0, inplace=True)
#df_store['Promo2SinceYear'].fillna(0, inplace=True)
#df_store['PromoInterval'].fillna(0, inplace=True)
#
#df_store.isnull().sum()