from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col
from joblib import dump

# create a SparkSession
spark = SparkSession.builder.getOrCreate()

#read the data
data = spark.read.csv('subset_data2.csv', header=True, inferSchema=True)
data = data.withColumn("flightDate", col("flightDate").cast("string"))
# data.show()

indexer = StringIndexer(inputCol="flightDate", outputCol="flightDate_indexed",  handleInvalid='keep')
flightDateModel = indexer.fit(data)
indexed_data= flightDateModel.transform(data)

indexer = StringIndexer(inputCol="startingAirport", outputCol="startingAirport_indexed")
startingAirportModel = indexer.fit(data)
indexed_data= startingAirportModel.transform(indexed_data)

indexer = StringIndexer(inputCol="destinationAirport", outputCol="destinationAirport_indexed")
destinationAirportModel = indexer.fit(data)
indexed_data= destinationAirportModel.transform(indexed_data)

# print("//////////////////////////////////////////////////")
# print("//////////////////////////////////////////////////")
# print("//////////////////////////////////////////////////")
# indexed_data.show()
# print("//////////////////////////////////////////////////")
# print("//////////////////////////////////////////////////")
# print("//////////////////////////////////////////////////")



# create features vector
feature_columns = indexed_data.columns[-3:] # here we omit the final column
assembler = VectorAssembler(inputCols=feature_columns,outputCol="features")
data_2 = assembler.transform(indexed_data)
# data_2.show()

train, test = data_2.randomSplit([0.7, 0.3])

algo = LinearRegression(featuresCol="features", labelCol="totalFare")
model = algo.fit(train)
model.save("ticket_price_pred.model")
flightDateModel.save("flightDateModel")
startingAirportModel.save("startingAirportModel")
destinationAirportModel.save("destinationAirportModel")

evaluation_summary = model.evaluate(test)
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")
# print(evaluation_summary.meanAbsoluteError)
# print(evaluation_summary.rootMeanSquaredError)
# print(evaluation_summary.r2)
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------------")

# def pred_ticket_price_in_date_start_end_airport(date, startingAirport, destinationAirport):
#     df = spark.createDataFrame([{"flightDate": date, "startingAirport": startingAirport, "destinationAirport": destinationAirport}])

#     fdJob = flightDateModel.transform(df)
#     saJob = startingAirportModel.transform(fdJob)
#     daJob = destinationAirportModel.transform(saJob)

#     data_3 = assembler.transform(daJob)

#     predictions = model.transform(data_3)

#     return predictions.first()[-1]

# price = pred_ticket_price_in_date_start_end_airport("2022-04-08", "BOS", "ATL")