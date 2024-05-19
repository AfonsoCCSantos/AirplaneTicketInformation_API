from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col

# create a SparkSession
spark = SparkSession.builder.getOrCreate()

#read the data
data = spark.read.csv('subset_data2.csv', header=True, inferSchema=True)
data = data.withColumn("flightDate", col("flightDate").cast("string"))
# data.show()

indexer = StringIndexer(inputCol="flightDate", outputCol="flightDate_indexed")
flightDateModel = indexer.fit(data)
indexed_data= flightDateModel.transform(data)

indexer = StringIndexer(inputCol="startingAirport", outputCol="startingAirport_indexed")
startingAirportModel = indexer.fit(data)
indexed_data= startingAirportModel.transform(indexed_data)

indexer = StringIndexer(inputCol="destinationAirport", outputCol="destinationAirport_indexed")
destinationAirportModel = indexer.fit(data)
indexed_data= destinationAirportModel.transform(indexed_data)

print("//////////////////////////////////////////////////")
print("//////////////////////////////////////////////////")
print("//////////////////////////////////////////////////")
indexed_data.show()
print("//////////////////////////////////////////////////")
print("//////////////////////////////////////////////////")
print("//////////////////////////////////////////////////")



# create features vector
feature_columns = indexed_data.columns[-3:] # here we omit the final column
print(feature_columns)
assembler = VectorAssembler(inputCols=feature_columns,outputCol="features")
data_2 = assembler.transform(indexed_data)
data_2.show()

train, test = data_2.randomSplit([0.7, 0.3])

algo = LinearRegression(featuresCol="features", labelCol="totalFare")
model = algo.fit(train)

evaluation_summary = model.evaluate(test)
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")
print(evaluation_summary.meanAbsoluteError)
print(evaluation_summary.rootMeanSquaredError)
print(evaluation_summary.r2)
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------")

# 2022-08-02|            PHL|               OAK
# [17.0,8.0,14.0]
# df_fd = spark.createDataFrame([
#     {"flightDate": "2022-08-02"}
# ])

# df_sa = spark.createDataFrame([
#     {"startingAirport": "PHL"}
# ])

# df_da = spark.createDataFrame([
#     {"destinationAirport": "OAK"}
# ])

df = spark.createDataFrame([{"flightDate": "2022-08-02", "startingAirport": "PHL", "destinationAirport": "OAK"}])

fdJob = flightDateModel.transform(df)
saJob = startingAirportModel.transform(fdJob)
daJob = destinationAirportModel.transform(saJob)


# print("*****************************************************************")
# print("*****************************************************************")
# print("*****************************************************************")
# print(fdJob.first()[-1]) # filtering out some
# # print(fdJob.select(fdJob.columns[-1]).collect()) # filtering out some
# print("*****************************************************************")
# print("*****************************************************************")
# print("*****************************************************************")

# vec = VectorAssembler(inputCols=feature_columns,outputCol="features")
data_3 = assembler.transform(daJob)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
predictions = model.transform(data_3)
print(predictions.first()[-1])


