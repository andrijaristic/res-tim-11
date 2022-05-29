from  classes import  DatabaseAnalytics

if __name__ == '__main__':
    databasecrudaddress = ('localhost',23000)
    databaseanalytics = DatabaseAnalytics(databasecrudaddress)
    databaseanalytics.run()