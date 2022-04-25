from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, BooleanType, MapType
from pyspark.sql.functions import col
from gharchive import GHArchive
from pathlib import Path


def getDate():
    date = input('\nEnter month and year (format: M/YYYY): ')
    month = date[0]
    year = date[2:7]
    if month == '2':
        if int(year) % 2 == 0:
            day = '29'
        else: day = '28'
    elif month in ['4', '6', '9', '11']:
        day = '30'
    else: day = '31'
    startDate = month + '/1/' + year
    endDate = month + '/' + day + '/' + year
    return startDate, endDate

def getRepository(df, repoName):
    return df.filter(col('repo.name') == repoName)

def countPRs(df):
    return df.filter(df.type == 'PullRequestEvent').count()

def countStars(df):
    watchEvents = df.filter(df.type == 'WatchEvent')
    watchEvents = watchEvents.select('actor.key').distinct().count()
    return watchEvents

def printReport(repoName, startDate, endDate, watchEvents, pullRequests):
    print('-' * 72)
    print('Repository name: ', repoName)
    print('Start date: ', startDate)
    print('End date: ', endDate)
    print('-' * 72)
    print('No of times repo was starred: ', watchEvents)
    print('Number of pull requests: ', pullRequests)

def exportReport(fileT, repoName, startDate, endDate, watchEvents, pullRequests):
    if fileT == '-csv':
        filename = 'report' + '.csv'
    else: filename = 'report' + '.txt'

    file = Path(filename)
    file.touch(exist_ok=True)

    with open(filename, 'w') as f:
        f.write('repoName,' + repoName)
        f.write('\nstartDate,' + startDate)
        f.write('\nendDate,' + endDate)
        f.write('\nwatchEvents,' + str(watchEvents))
        f.write('\npullRequests,' + str(pullRequests))

def txtReport():
    pass




if __name__ == '__main__':
    startDate, endDate = getDate()

    spark = SparkSession.builder.appName('GH Archive').getOrCreate()

    schema = StructType([ 
        StructField('actor', MapType(StringType(), StringType(), True), True),
        StructField('created_at', StringType(), True),
        StructField('id', StringType(), True),
        StructField('payload', MapType(StringType(), StringType(), True), True),
        StructField('public', BooleanType(), True),
        StructField('repo', MapType(StringType(), StringType(), True), True),
        StructField('type', StringType(), True)
        ])

    gh = GHArchive()
    getRepo = gh.get(startDate, endDate)

    dataDict = getRepo.to_dict_list()

    df = spark.createDataFrame(dataDict, schema=schema)

    ans = '-list'

    print('\nTo list all available repositories, enter "-list".')
    while ans == '-list':
        ans = input('Enter repo name: ')

        if ans == '-list':
           availableRepos = df.select('repo.name').distinct().rdd.map(lambda r: r[0]).collect()
           for repo in availableRepos:
               print('- ', repo)
        else:
            repoDF = getRepository(df, ans)
    
    print("Select format of the report:\n \
        -sc   show report in terminal\n \
        -csv  export to csv\n \
        -txt  export to txt")
    format = input('Enter selected format: ')

    if format == '-sc':
        printReport(ans, startDate, 'x', countStars(repoDF), countPRs(repoDF))
    else:
        exportReport(format, ans, startDate, 'x', countStars(repoDF), countPRs(repoDF))