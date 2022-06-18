from  database_analitics import  DatabaseAnalytics

if __name__ == '__main__':
    databasecrudaddress = ('localhost',23000)
    databaseanalytics = DatabaseAnalytics()
    databaseanalytics.connect_to_databasecrud(databasecrudaddress)
    databaseanalytics.run()
