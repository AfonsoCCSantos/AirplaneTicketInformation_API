from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col

# create a SparkSession
spark = SparkSession.builder.getOrCreate()

#read the data
data = spark.read.csv('../../spark/subset_data.csv', header=True, inferSchema=True)
data = data.withColumn("flightDate", col("flightDate").cast("string"))
# data.show()

indexer = StringIndexer(inputCol="flightDate", outputCol="flightDate_indexed")
indexer_model = indexer.fit(data)
indexed_data= indexer_model.transform(data)
indexer = StringIndexer(inputCol="startingAirport", outputCol="startingAirport_indexed")
indexer_model = indexer.fit(data)
indexed_data= indexer_model.transform(indexed_data)
indexer = StringIndexer(inputCol="destinationAirport", outputCol="destinationAirport_indexed")
indexer_model = indexer.fit(data)
indexed_data= indexer_model.transform(indexed_data)

# indexed_data.show()



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
print(evaluation_summary.meanAbsoluteError)
print(evaluation_summary.rootMeanSquaredError)
print(evaluation_summary.r2)
