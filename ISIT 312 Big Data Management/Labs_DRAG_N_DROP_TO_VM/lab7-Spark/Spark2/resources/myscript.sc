import spark.implicits._
val person = Seq((0, "Bill Chambers", 0, Seq(100)),(1, "Matei Zaharia", 1, Seq(500, 250, 100)),(2, "Michael Armbrust", 1, Seq(250, 100))).toDF("id", "name", "graduate_program", "spark_status")
